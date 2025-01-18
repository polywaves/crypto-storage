import time
from app.utils.logger_util import logger


def response(data: dict, start_time) -> dict:
  speed = time.time() - start_time
  data["duration"] = speed

  logger.debug(f"RESPONSE TIME: {speed} s")

  return data