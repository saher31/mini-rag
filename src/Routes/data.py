from fastapi import APIRouter,Depends,UploadFile,status,Request
from fastapi.responses import JSONResponse
import os 
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessingRequest
from models.ProjectModel import ProjectModel 
from models.db_schemes import DataChunk
from models.ChunkModel import ChunkModel

logger = logging.getLogger('uvicorn.error')

data_router=APIRouter(
    prefix='/api/v1/data',
    tags=['api_v1','data'],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request:Request,project_id:str,file:UploadFile,
    app_settings: Settings = Depends(get_settings)):

    project_model=ProjectModel(
        db_client=request.app.db_client
     )
    
    project = await project_model.get_project_or_create_one(project_id=project_id)
    

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
        "file_id":file_id,
        }) 

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str,processing_request: ProcessingRequest,request:Request):
    file_id=processing_request.file_id
    chunk_size=processing_request.chunk_size
    overlap_size=processing_request.overlap_size
    do_reset=processing_request.do_reset
    
    project_model=ProjectModel(
        db_client=request.app.db_client
    )
    project = await project_model.get_project_or_create_one(project_id=project_id)

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
    
    file_chunks_record=[
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id
        ) for i, chunk in enumerate(file_chunks) 
    ] 

    chunk_model=ChunkModel( 
        db_client=request.app.db_client
    )

    if do_reset==1:
        _ = await chunk_model.delete_chunks_by_project_id(project_id=project.id)

    
    no_records = await chunk_model.create_multiple_chunks(chunks=file_chunks_record)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"is_valid":True , "result_signal":ResponseSignal.PROCESSING_SUCCESSFULLY.value,
        "number":no_records
        })