# app/core/schemas/ocr.py

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Location(BaseModel):
    continent: Dict[str, Any]
    country: Dict[str, Any]
    location: Dict[str, Any]
    registered_country: Dict[str, Any]

class AmountField(BaseModel):
    data: Optional[float]
    confidenceLevel: Optional[float]
    text: Optional[str]
    index: Optional[int]
    keyword: Optional[str]
    currencyCode: Optional[str]
    regions: Optional[List[List[Dict[str, int]]]]

class DateField(BaseModel):
    data: Optional[str]
    confidenceLevel: Optional[float]
    text: Optional[str]
    index: Optional[int]
    regions: Optional[List[List[Dict[str, int]]]]

class TextField(BaseModel):
    text: Optional[str]
    regions: Optional[List[Dict[str, int]]]

class EntityProductLineItem(BaseModel):
    name: Dict[str, Any]
    totalPrice: Dict[str, Any]

class Entities(BaseModel):
    productLineItems: Optional[List[EntityProductLineItem]]
    IBAN: Optional[Dict[str, Any]]
    invoiceNumber: Optional[Dict[str, Any]]
    multiTaxLineItems: Optional[List[Any]]
    receiptNumber: Optional[Dict[str, Any]]
    last4: Optional[Dict[str, Any]]

class OCRDataInner(BaseModel):
    location: Optional[Location]
    totalAmount: Optional[AmountField]
    taxAmount: Optional[AmountField]
    discountAmount: Optional[AmountField]
    paidAmount: Optional[AmountField]
    confidenceLevel: Optional[float]
    date: Optional[DateField]
    dueDate: Optional[DateField]
    text: Optional[TextField]
    amounts: Optional[List[AmountField]]
    numbers: Optional[List[Any]]
    entities: Optional[Entities]
    lineAmounts: Optional[List[Any]]
    itemsCount: Optional[Dict[str, Any]]
    paymentType: Optional[Dict[str, Any]]
    trackingId: Optional[str]
    merchantName: Optional[Dict[str, Any]]
    merchantAddress: Optional[Dict[str, Any]]
    merchantCity: Optional[Dict[str, Any]]
    merchantState: Optional[Dict[str, Any]]
    merchantCountryCode: Optional[Dict[str, Any]]
    merchantTypes: Optional[Dict[str, Any]]
    merchantPostalCode: Optional[Dict[str, Any]]
    merchantTaxId: Optional[Dict[str, Any]]
    elapsed: Optional[float]

class OCRData(BaseModel):
    ocr_data: OCRDataInner
