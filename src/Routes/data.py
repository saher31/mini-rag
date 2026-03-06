from fastapi import APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessingRequest
 

logger = logging.getLogger('uvicorn.error')

data_router=APIRouter(
    prefix='/api/v1/data',
    tags=['api_v1','data'],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id:str,file:UploadFile,
    app_settings: Settings = Depends(get_settings)):
    #validate the file properties
    data_controller=DataController()
    is_valid , result_signal  = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"is_valid":is_valid , "result_signal":result_signal}) 
    
    project_dir_path=ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(orig_file_name=file.filename,project_id=project_id)
    try:
        async with aiofiles.open(file_path,'wb') as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"is_valid":False , "result_signal":ResponseSignal.FILE_UPLOAD_FAILED.value})
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"is_valid":is_valid , 
        "result_signal":ResponseSignal.FILE_UPLOADED_SUCCESSFULLY.value,
        "file_id":file_id}) 

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str,processing_request: ProcessingRequest,):
    file_id=processing_request.file_id
    chunk_size=processing_request.chunk_size
    overlap_size=processing_request.overlap_size
    
     
    precess_controller= ProcessController(project_id=project_id)
    file_content=precess_controller.get_file_content(file_id=file_id)
    file_chunks=precess_controller.process_file_content(
        file_content=file_content,file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size)

    if file_chunks is None or len(file_chunks)==0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"is_valid":False , "result_signal":ResponseSignal.PROCESSING_FAILED.value})
    
    return file_chunks