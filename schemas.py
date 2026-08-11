from pydantic import ConfigDict, BaseModel, Field
from datetime import datetime

class NoteBase(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    date_posted: datetime

class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1)
    content: str | None = Field(default=None, min_length=1)