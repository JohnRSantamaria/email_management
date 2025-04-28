import uvicorn
from app.core.settings import settings
import os

if __name__ == "__main__":
    host = os.getenv("HOST", settings.HOST)
    port = int(os.getenv("PORT", settings.PORT))
    debug = settings.DEBUG

    uvicorn.run("app.main:app", host=host, port=port, reload=debug)
