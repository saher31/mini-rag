from pydantic import BaseModel, Field , validator
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    _id: Optional[ObjectId] = Field(...,min_length=1)
    project_id : str
    
    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum() :

            raise ValueError('project_id must be alphanumeric and not empty')

        return value

    class Config:
        arbitrary_types_allowed = True    