import os
from dotenv import dotenv_values
from yc_lockbox import YandexLockboxClient, Secret


env = dotenv_values(".env")
config = env if env else os.environ

## Get encryption key
encryption_key_id = "ENCRYPTION_KEY"
lockbox = YandexLockboxClient(config["YC_OAUTH_TOKEN"])

def get_encryption_key():
  secret: Secret = lockbox.get_secret(config["YC_LOCKBOX_SECRET_ID"])
  payload = secret.payload(version_id=secret.current_version.id)
  entry = payload[encryption_key_id]

  return entry.reveal_text_value()