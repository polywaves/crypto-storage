from fastapi import APIRouter
from app.api.v1 import storage


router = APIRouter()

router.include_router(storage.router, prefix='/storage')