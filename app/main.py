# app\main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from app.routes import document

def format_error_response(error_message: str, error_type: str = "InternalError"):
    return {
        "detail": error_message,
        "error_type": error_type,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

app = FastAPI()

# Handler para errores HTTPException (por ejemplo 404, 403, etc.)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=format_error_response(
            error_message=str(exc.detail),
            error_type="HTTPException"
        )
    )


# Handler para errores generales (cualquier error no manejado)
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=format_error_response(
            error_message=str(exc),
            error_type="Exception"
        )
    )


app.include_router(document.router)
