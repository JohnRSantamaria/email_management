import dropbox
from dropbox.files import WriteMode
from .base import FileUploader
from app.core.settings import settings


class DropboxUploader(FileUploader):
    def __init__(self):
        self.dbx = dropbox.Dropbox(
            oauth2_access_token=settings.DROPBOX_ACCESS_TOKEN,
            oauth2_refresh_token=settings.DROPBOX_REFRESH_TOKEN,
            app_key=settings.DROPBOX_APP_KEY,
            app_secret=settings.DROPBOX_APP_SECRET,
        )

    def upload(self, local_path: str, remote_path: str):
        with open(local_path, "rb") as f:
            self.dbx.files_upload(f.read(), remote_path, mode=WriteMode("overwrite"))
