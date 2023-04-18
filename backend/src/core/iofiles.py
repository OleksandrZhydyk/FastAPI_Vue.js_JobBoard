import aioboto3
import aiofiles
import logging
import time

from botocore.exceptions import ClientError
from fastapi import UploadFile

from core.config import Config


async def upload_file(sub_path: str, file: UploadFile):
    if Config.USE_S3 == "True":
        session = aioboto3.Session(
            aws_access_key_id=Config.AWS_ACCESS_KEY,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        async with session.client("s3") as s3:
            try:
                aws_s3_file_path = f'{Config.AWS_MEDIA_LOCATION}/{sub_path}/{time.time()}_{file.filename}'
                await s3.upload_fileobj(
                    file,
                    Config.AWS_STORAGE_BUCKET_NAME,
                    aws_s3_file_path
                )
                return f'/{aws_s3_file_path}'
            except ClientError as e:
                logging.error(e)
                return None
    else:
        path_for_saving = f'{Config.STATIC_ROOT}/{sub_path}/{time.time()}_{file.filename}'
        try:
            async with aiofiles.open(path_for_saving, 'wb') as f:
                content = await file.read()
                await f.write(content)
        except Exception as e:
            print(e)
            return None

        return f'{Config.LOCAL_ORIGIN}/{path_for_saving}'
