from typing import Annotated
from fastapi import File, UploadFile
from app.core.constants.schemas.odoo import InvoiceSchema
from app.core.utils.extractors.invoice_extractor import InvoiceExtractor
from pydantic import ValidationError

from src.utils.save_document import save_file


def count_empty_fields(data):
    empty_fields = 0
    for key, value in data.items():
        if value in (None, "", [], {}, ()):
            empty_fields += 1
    return empty_fields


async def proces_document(payload: dict, file: Annotated[UploadFile, File(...)]):

    extractor = InvoiceExtractor(json_data=payload)
    main_fields = extractor.extract_main_fields()

    try:
        valid_fields = InvoiceSchema(**main_fields)
    except ValidationError:
        if count_empty_fields(main_fields) > 6:
            return {"type": "Error", "path_folder": "", "data": main_fields}
        else:
            return {"type": "Ticket", "path_folder": "", "data": main_fields}
    except Exception as e:
        raise RuntimeError(f"Unexpected error during validation: {e}") from e

    return await save_file(valid_fields, file)
