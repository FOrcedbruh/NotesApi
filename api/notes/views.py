from fastapi import APIRouter, Depends, HTTPException, status
from . import actions
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CreateNote
from core import db_core
from api.auth.actions import get_current_auth_user
from api.auth.schemas import UserSchema
from .actions import noteInParams

router = APIRouter(tags=["Notes"])



@router.get("/")
async def get_notes(
    authUser: UserSchema = Depends(get_current_auth_user),
    session: AsyncSession = Depends(db_core.session_creation)
):
    user_id: int = authUser.id
    return await actions.get_notes(session=session, user_id=user_id)


@router.post("/create")
async def create_note(
    note_in: CreateNote = Depends(noteInParams),
    session: AsyncSession = Depends(db_core.session_creation)
):
    return await actions.create_note(session=session, note_in=note_in)


@router.get("/{note_id}")
async def get_note_by_id(
        note_id: int,
        authUser: UserSchema = Depends(get_current_auth_user),
        session: AsyncSession = Depends(db_core.session_creation)
    ):
        return await actions.get_note_by_id(session=session, note_id=note_id, user_id=authUser.id)
            
       



