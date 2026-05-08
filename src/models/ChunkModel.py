from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk 
from .enums.DataBaseEnums import DataBaseEnums
from bson import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnums.COLLECTION_CHUNK_NAME.value] 

    async def create_chunk(self, chunk_obj: DataChunk):
        chunk_dict = chunk_obj.model_dump(by_alias=True, exclude_none=True)
        result = await self.collection.insert_one(chunk_dict)
        chunk_obj.id = result.inserted_id
        return chunk_obj 

    async def get_chunk(self,chunk_id: str):
        record = await self.collection.find_one({
            '_id': ObjectId(chunk_id)
        })   
        if record is None:
            return None
        return DataChunk(**record)

    async def create_multiple_chunks(self, chunks: list,batch_size: int = 100):
        
        for i in range(0,len(chunks),batch_size):
            batch= chunks[i:i+batch_size]
            operation=[
            InsertOne(chunk.model_dump(by_alias=True, exclude_unset=True)) 
            for chunk in batch]

            await self.collection.bulk_write(operation)
        return len(chunks)

    async def delete_chunks_by_project_id(self,project_id:ObjectId): 

        result = await self.collection.delete_many({
            'chunk_project_id': project_id
        })

        return result.deleted_count
