# backend/src/oaa/models/schemas.py

from pydantic import BaseModel

class ProjectRequest(BaseModel):
    project_name: str
    project_path: str
    source_code: str