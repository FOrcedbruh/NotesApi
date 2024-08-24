from core.models import Note, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, delete
from .schemas import CreateNote, ReadNote
from fastapi import Form, Depends, HTTPException, status
from api.auth.actions import get_current_auth_user
from api.auth.schemas import UserSchema


async def get_notes(session: AsyncSession, user_id: int) -> list[ReadNote]:
    data = select(Note).filter(Note.user_id == user_id)
    res: Result = await session.execute(data)
    notes =  res.scalars().all()
    
    
    return list(notes)


async def get_note_by_id(session: AsyncSession, note_id: int, user_id: int) -> ReadNote:
    note: Note = await session.get(Note, note_id)
    if note.user_id == user_id:
        return note
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Acess denied"
    )



def noteInParams(title: str = Form(), body: str = Form(), authUser: UserSchema = Depends(get_current_auth_user)):
    
    user_id: int = authUser.id
    
    return {
        "title": title,
        "body": body,
        "user_id": user_id
    }


async def create_note(session: AsyncSession, note_in: CreateNote) -> dict:
    note = Note(**note_in)
    session.add(note)
    
    
    await session.commit()
    
    return {
        "status": status.HTTP_201_CREATED,
        "message": f"Note {note.title} created"
    }


async def erase_note_by_id(session: AsyncSession, note_id: int, user_id: int):
    
    NoteToErase: Note = await session.get(Note, note_id)
    if NoteToErase.user_id == user_id:
        await session.delete(NoteToErase)
        await session.commit()

        return {
            "status": status.HTTP_200_OK,
            "message": f"Successfully delete {NoteToErase.title}"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Acces denied"
    )
    
        