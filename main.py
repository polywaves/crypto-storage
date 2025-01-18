import os
from time import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from app.api import v1
from app.config import config
from app.utils.logger_util import logger


app = FastAPI(
  docs_url = None,
  redirect_slashes=False
)  


@app.on_event("startup")
async def startup_event():
  logger.info("App started")


@app.on_event("shutdown")
async def shutdown_event():
  logger.info("App shutted down")


if config["MODE"] == 'development':
  logger.debug("Development mode")
  app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
  )


@app.middleware("http")
async def http_processing(request: Request, call_next) -> any:
  url = str(request.url)
  client_ip = request.client.host

  if "x-real-ip" in request.headers:
    client_ip = request.headers["x-real-ip"]

    logger.info(f"REQUESTED BY CLIENT IP: {client_ip}")

    ip_list = config["API_ALLOW_IP_LIST"].split(',')
    route_list = config["API_EXCLUDE_ROUTES"].split(',')

    if len(ip_list) and client_ip not in ip_list:
      found = False
      for route in route_list:
        if route in url:
          found = True

      if not found:
        return JSONResponse(content="Access denied", status_code=403)
  
  try:
    response = await call_next(request)
  except Exception as e:
    error = str(e)
    response = JSONResponse(content=error, status_code=500)

  return response


app.include_router(v1.router, prefix='/api/v1')


@app.get("/apidoc", include_in_schema=False)
async def custom_swagger_ui_html():
  return get_swagger_ui_html(
    openapi_url=app.openapi_url,
    title=f"{app.title} - Swagger UI"
  )


@app.get("/health")
def health_check():
  return {
    "status": "healthy"
  }
