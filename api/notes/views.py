from fastapi import APIRouter, Depends
from . import actions
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CreateNote
from core import db_core

router = APIRouter(tags=["Notes"])



@router.get("/")
async def get_notes(
    session: AsyncSession = Depends(db_core.session_creation)
):
    return await actions.get_notes(session=session)


@router.post("/")
async def create_note(
    note_in: CreateNote,
    session: AsyncSession = Depends(db_core.session_creation)
):
    return await actions.create_note(session=session, note_in=note_in)


@router.get("/{note_id}")
async def get_note_by_id(
    note_id: int,
    session: AsyncSession = Depends(db_core.session_creation)
    ):
    return await actions.get_note_by_id(session=session, note_id=note_id)



