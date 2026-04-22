from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class NoteCreate(BaseModel):
    title: str
    note: str

class NoteResponse(BaseModel):
    id: int
    title: str
    note: str

    class Config:
        from_attributes = True

class NoteUpdate(BaseModel):
    title: str | None = None
    note: str | None = None
    isArchive: bool | None = None
    isPinned: bool | None = None