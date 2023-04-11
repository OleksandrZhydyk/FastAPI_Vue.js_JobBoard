import aiofiles
import time
from fastapi import UploadFile

from core.config import Config


async def upload_file(sub_path: str, file: UploadFile):
    path_for_saving = f'{Config.STATIC_ROOT}/{sub_path}/{time.time()}_{file.filename}'
    try:
        async with aiofiles.open(path_for_saving, 'wb') as f:
            content = await file.read()
            await f.write(content)
    except Exception as e:
        print(e)
        return None

    return f'{Config.HOSTED_DOMAIN}/{path_for_saving}'
