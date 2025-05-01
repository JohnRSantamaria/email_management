import os
import uuid
import dropbox
from dropbox.files import WriteMode
from pydantic import ValidationError
from app.core.constants.schemas.odoo import InvoiceSchema
from app.core.utils.extractors.invoice_extractor import InvoiceExtractor
from app.core.settings import settings


def upload_to_dropbox(local_path: str, dropbox_path: str):
    access_token = settings.ACCESS_TOKEN_DROPBOX
    if not access_token:
        raise EnvironmentError(
            "ACCESS_TOKEN_DROPBOX is not set in environment variables"
        )

    dbx = dropbox.Dropbox(access_token)
    print(dbx.users_get_current_account())
    with open(local_path, "rb") as f:
        dbx.files_upload(f.read(), dropbox_path, mode=WriteMode("overwrite"))


def save_file(valid_fields: InvoiceSchema):
    try:
        BASE_FILE = rf"src/data"
        MONTHS = {
            1: "Enero",
            2: "Febrero",
            3: "Marzo",
            4: "Abril",
            5: "Mayo",
            6: "Junio",
            7: "Julio",
            8: "Agosto",
            9: "Septiembre",
            10: "Octubre",
            11: "Noviembre",
            12: "Diciembre",
        }

        date = valid_fields.invoice_date
        year = date.year
        quarter = f"Q{(date.month - 1) // 3 + 1}"
        month_f = f"{str(date.month).zfill(2)}-{MONTHS[date.month]}"
        path_folder = os.path.join(BASE_FILE, str(year), quarter, month_f)
        os.makedirs(path_folder, exist_ok=True)

        guid = uuid.uuid4()
        file_name = f"{valid_fields.tax_identification_supplier}_{guid}.json"
        full_path = os.path.join(path_folder, file_name)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(valid_fields.model_dump_json(indent=4))

        # Subir a Dropbox
        dropbox_path = f"/{year}/{quarter}/{month_f}/{file_name}"
        upload_to_dropbox(full_path, dropbox_path)

        return {
            "type": "Invoice",
            "path_folder": f"{year}/{quarter}/{month_f}",
            "data": valid_fields.model_dump(),
        }

    except Exception as e:
        raise RuntimeError(f"Error saving or uploading file: {e}") from e


async def proces_document(file: dict):
    extractor = InvoiceExtractor(json_data=file)
    main_fields = extractor.extract_main_fields()

    try:
        valid_fields = InvoiceSchema(**main_fields)
    except ValidationError:
        return {"type": "Ticket", "path_folder": "", "data": main_fields}
    except Exception as e:
        raise RuntimeError(f"Unexpected error during validation: {e}") from e

    return save_file(valid_fields)
