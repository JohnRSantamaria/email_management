import os
import uuid

from typing import Annotated
from fastapi import File, UploadFile
from app.core.constants.schemas.odoo import InvoiceSchema

from src.uploaders.factory import get_uploader
from src.utils.path_builder import PathBuilder


async def save_file(
    valid_fields: InvoiceSchema,
    file: Annotated[UploadFile, File(...)],
    uploader_name="dropbox",
):
    guid = uuid.uuid4()
    file_ext = os.path.splitext(file.filename or "")[-1]
    original_filename = f"{valid_fields.tax_identification_supplier}_{guid}{file_ext}"
    file_path = os.path.join(original_filename)

    try:
        with open(file_path, "wb") as f_out:
            f_out.write(await file.read())

        path_builder = PathBuilder()
        remote_path = path_builder.build(valid_fields.invoice_date)

        uploader = get_uploader(uploader_name)
        uploader.upload(file_path, f"{remote_path}/{original_filename}")

        return {
            "type": "Invoice",
            "path_folder": remote_path.strip("/"),
            "data": valid_fields.model_dump(),
        }

    except Exception as e:
        raise RuntimeError(f"Error saving or uploading file: {e}") from e
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
