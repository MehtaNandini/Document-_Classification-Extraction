import os
import tempfile
from fastapi import UploadFile

async def save_upload_file_tmp(upload_file: UploadFile) -> str:
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        fd, tmp_path = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(fd, 'wb') as f:
            content = await upload_file.read()
            f.write(content)
        return tmp_path
    finally:
        await upload_file.seek(0)
