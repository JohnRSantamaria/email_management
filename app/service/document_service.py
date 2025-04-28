import os
import uuid
from app.core.constants.schemas.odoo import InvoiceSchema
from app.core.utils.extractors.invoice_extractor import InvoiceExtractor
from pydantic import ValidationError


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

        with open(full_path, "w") as f:
            f.write(valid_fields.model_dump_json(indent=4))

        return {
            "type": "Invoice",
            "path_folder": f"{str(year)}/{quarter}/{month_f}",
            "data": valid_fields.model_dump(),
        }
    except Exception as e:
        raise e


async def proces_document(file: dict):

    extractor = InvoiceExtractor(json_data=file)
    main_fields = extractor.extract_main_fields()

    try:
        valid_fields = InvoiceSchema(**main_fields)
    except ValidationError as ve:
        return {"type": "Ticket", "path_folder": "", "data": main_fields}
    except Exception as e:
        raise e

    return save_file(valid_fields)
