from .BaseDataModel import BaseDataModel
from .db_schemes import Project 
from .enums.DataBaseEnums import DataBaseEnums

class ProjectModel(BaseDataModel):
    
    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnums.COLLECTION_PROJECT_NAME.value] 

    async def create_project(self, project_obj: Project):
        # بنستخدم by_alias=True عشان يحول id لـ _id للمونجو
        project_dict = project_obj.model_dump(by_alias=True, exclude_unset=True)
        result = await self.collection.insert_one(project_dict)
        project_obj.id = result.inserted_id
        return project_obj 

    async def get_project_or_create_one(self, project_id: str):
        record = await self.collection.find_one({
            'project_id': project_id
        })   
        
        if record is None:
            # هنا التغيير المهم: بنستخدم اسم الكلاس (Project) 
            # وبنخزن في متغير اسمه (new_project) عشان م يحصلش UnboundLocalError
            new_project = Project(project_id=project_id)
            inserted_project = await self.create_project(project_obj=new_project)
            return inserted_project 

        # بنستخدم **record عشان نبعت الداتا للكلاس
        return Project(**record)            

    async def get_all_projects(self, page: int = 1, page_size: int = 10): 
        total_documents = await self.collection.count_documents({})
 
        total_pages = (total_documents + page_size - 1) // page_size

        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))

        return projects, total_pages