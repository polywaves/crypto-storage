import io
import uuid
from time import time
from unidecode import unidecode
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from cryptography.fernet import Fernet
from app.config import config
from app.providers.s3 import s3
from app.utils.logger_util import logger
from app.utils.response_util import response

router = APIRouter()


@router.put("/file", tags=["Put file"])
async def put_file(encryption_key: str, file: UploadFile = File()):
  start_time = time()
  id = str(uuid.uuid4())

  ## Make encrypted file stream
  fernet = Fernet(encryption_key)

  stream = await file.read()
  encrypted_stream = fernet.encrypt(stream)

  ## Upload encrypted file stream to s3
  metadata = {
    "name": unidecode(file.filename),
    "content_type": file.content_type
  }

  logger.debug(metadata)

  s3.upload_fileobj(io.BytesIO(encrypted_stream), config["S3_BUCKET"], id, ExtraArgs={
    "Metadata": metadata
  })

  return response({
    "id": id
  }, start_time=start_time)


@router.get("/file", tags=["Get file"])
async def get_file(id: str, encryption_key: str):
  ## Exec
  fernet = Fernet(encryption_key)

  file = s3.get_object(Bucket=config["S3_BUCKET"], Key=id)
  metadata = file["Metadata"]
  stream = file["Body"].read()
  decrypted_stream = fernet.decrypt(stream)
  
  name = metadata["name"]
  headers = {
    "Content-Disposition": f"attachment; filename={name}"
  }

  return Response(content=decrypted_stream, media_type=metadata["content_type"], headers=headers)


@router.get("/new_encryption_key", tags=["Get new encryption key"])
async def new_encryption_key():
  start_time = time()

  ## Exec
  encryption_key = Fernet.generate_key()

  return response({
    "encryption_key": encryption_key
  }, start_time=start_time)