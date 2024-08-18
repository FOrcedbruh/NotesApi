from pydantic import BaseModel, Field, ConfigDict





class NoteBase(BaseModel):
    title: str = Field(max_length=10)
    body: str
    user_id: int
    
    
class ReadNote(NoteBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
    
    
class CreateNote(NoteBase):
    pass
    