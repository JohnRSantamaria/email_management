import re
import json


def contains_number(text: str): 
    """Verify if the code has at least one number"""
    return any(c.isdigit()for c in text) 


def extract_code(text: str, regex):
    """Extracts a code that contains al least one number"""

    matches = regex.findall(text)
    return [m for m in matches if contains_number(m)]


def extraer_informacion(json_data):
    """
    RegEx: 

    NIF : NIF\s\w+ 
        - NIF → busca exactamente las letras NIF.
        - \s → un espacio en blanco.
        - \w+ → una o más letras, números o guiones bajos (lo normal en un NIF).


    
    """
    patron_nif = r'(?i)(?:^|\\n|\s)N\.?\s*I\.?\s*F\.?\s+([^\s|\\]+)'
    patron_cif = r'(?i)(?:^|\\n|\s)C\.?\s*I\.?\s*F\.?\s+([^\s|\\]+)'
    patron_vat = r'(?i)(?:^|\\n|\s)V\.?\s*A\.?\s*T(?:\s*No:?)?(?:\s*ID:?)?\.?\s+([^\s|\\]+)'
    patron_cf = r'(?i)(?:^|\\n|\s)C\.?\s*F(?:\s*No:?)?(?:\s*ID:?)?\.?\s+([^\s|\\]+)'
    patron_es = r'(?i)(?:^|\\n|\s)E\.?\s*S(?:\s*No:?)?(?:\s*ID:?)?\.?([^\s|\\]+)' 
    # TODO : Verificacion NO debe ser alfabetico, SOLO Alfanumerico o numerico.

    ocr_data = json_data.get("ocr_data", {})


    # Extrer los codigos fiscales presentes. 
    buyers_tax_identification = (
        ocr_data.get("text", {}).get("text", "")                                
    )
   


    # Extraer campos principales
    partner_id = (
        ocr_data.get("entities", {}).get("merchantName", {}).get("data") or
        ocr_data.get("merchantName", {}).get("data", "")
    )

    supplier_tax_identification = (
        ocr_data.get("merchantVerification", {}).get("data", {}).get("verificationId") or
        ocr_data.get("merchantTaxId", {}).get("data", "")
    ) 

    invoice_date = ocr_data.get("date", {}).get("data", "")
    invoice_number = (
        ocr_data.get("entities", {}).get("invoiceNumber", {}).get("data") or
        ocr_data.get("entities", {}).get("receiptNumber", {}).get("data", "")
    )
    amount_total = ocr_data.get("totalAmount", {}).get("data", 0.0)
    amount_untaxed = None
    tax_amount = ocr_data.get("taxAmount", {}).get("data", 0.0)

    # Buscar base imponible en `amounts`
    for amount in ocr_data.get("amounts", []):
        if amount.get("currencyCode") in ["EUR", "USD"] and amount.get("data") not in [amount_total, tax_amount]:
            amount_untaxed = amount.get("data")
            break

    if amount_untaxed is None:
        # Si no hay, calcularlo
        amount_untaxed = round(amount_total - tax_amount, 2)

    # Extraer líneas
    lines = []
    for item in ocr_data.get("entities", {}).get("productLineItems", []):
        lines.append({
            "description": item["data"].get("name", {}).get("data", ""),
            "quantity": item["data"].get("quantity", {}).get("data", 1),
            "price_unit": item["data"].get("totalPrice", {}).get("data", 0.0)
        })

    # Si no encuentra líneas pero hay amounts y texto, crea una línea genérica
    if not lines and "text" in ocr_data:
        lines.append({
            "description": "Servicio o Producto",
            "quantity": 1,
            "price_unit": amount_total
        })

    return {
        "partner_id": partner_id,
        "invoice_date": invoice_date[:10],
        "invoice_number": invoice_number,
        "amount_total": amount_total,
        "supplier_tax_identification":supplier_tax_identification,
        "amount_untaxed": amount_untaxed,        
        "tax_amount": tax_amount,
        "lines": lines
    }

# Ejemplo de uso

path = rf'uploaded_files\distribusiones.json'

with open(path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    resultado = extraer_informacion(data)
    # print(json.dumps(resultado, indent=2, ensure_ascii=False))
