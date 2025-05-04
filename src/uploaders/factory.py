from .dropbox import DropboxUploader
from .base import FileUploader


def get_uploader(name: str) -> FileUploader:
    if name == "dropbox":
        return DropboxUploader()
    raise ValueError(f"Unknown uploader: {name}")
