import colorlog
import sys
import json

logger = colorlog.getLogger(__name__)
logger.setLevel(colorlog.DEBUG)
formatter = colorlog.ColoredFormatter(
  "%(log_color)s%(levelname)-8s%(reset)s %(purple)s%(message)s",
  datefmt=None,
  reset=True,
  log_colors={
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'red',
  }
)

stream_handler = colorlog.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

logger.json = lambda text: logger.debug(json.dumps(text, indent=4, sort_keys=True, default=str))