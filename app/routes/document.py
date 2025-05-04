# app\routes\document.py
import json
from fastapi import APIRouter
from app.service.document_service import proces_document
from typing import Annotated
from fastapi import File, UploadFile, Form


router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post("/ocr-invoices")
async def ocr_on_invoices(
    payload: Annotated[str, Form(...)], file: Annotated[UploadFile, File(...)]
):
    try:
        parsed_payload = json.loads(payload)
    except json.JSONDecodeError:
        return {"error": "Payload is not a valid JSON"}

    return await proces_document(parsed_payload, file)
