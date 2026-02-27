from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field

class OutputSchema(BaseModel):
    repo_title: str = Field(..., min_length=1)
    description: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    url_to_repo: HttpUrl

class ChatOutput(BaseModel):
    """Respuesta estructurada con los repositorios encontrados"""
    repositories: List[OutputSchema]
    
class BodyParams(BaseModel):
    prompt: str = Field(..., min_length=1)
    programming_language: Optional[str] = Field(default=None, pattern="^(python|javascript)$")