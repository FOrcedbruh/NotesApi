from core.models import Note
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from .schemas import CreateNote, ReadNote


async def get_notes(session: AsyncSession) -> list[ReadNote]:
    data = select(Note).order_by(Note.id)
    res: Result = await session.execute(data)
    notes =  res.scalars().all()
    
    
    return list(notes)


async def get_note_by_id(session: AsyncSession, note_id: int) -> ReadNote:
    return await session.get(Note, note_id)


async def create_note(session: AsyncSession, note_in: CreateNote) -> Note:
    note = Note(**note_in.model_dump())
    session.add(note)
    
    
    await session.commit()
    
    return note