from fastapi import APIRouter
from .notes.views import router as notesRouter
from .auth.views import router as authRouter


router = APIRouter()
router.include_router(router=notesRouter, prefix="/notes")
router.include_router(router=authRouter)

