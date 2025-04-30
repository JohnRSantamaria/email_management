# app\routes\document.py
from fastapi import APIRouter
from app.service.document_service import proces_document

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/upload")
async def upload_document(payload: dict):
    response = await proces_document(payload)
    return {"response": response}
