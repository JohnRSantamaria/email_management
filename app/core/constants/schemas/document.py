from pydantic import BaseModel

class DocumentMetaData(BaseModel): 
    filename: str
    content_type: str