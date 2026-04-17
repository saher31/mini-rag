from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson import ObjectId

class Project(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    project_id: str

    @field_validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric and not empty')
        return value

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True