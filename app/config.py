import os
from dotenv import dotenv_values


env = dotenv_values(".env")
config = env if env else os.environ