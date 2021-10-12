# https://pypi.org/project/python-dotenv/
# https://www.askpython.com/python/python-dotenv-module

import os
from pprint import pprint as pp
from pathlib import Path
from dotenv import load_dotenv, dotenv_values, find_dotenv


# pp(os.environ)
curr_dir = Path(__file__).parent
private_env_path = curr_dir / ".env1"
shared_env_path = curr_dir / ".env.shared"

# find path of .env file
print("Env from .env (default) file - ")
print(find_dotenv())

load_dotenv(find_dotenv())
print(os.environ.get("DOMAIN"))
print(os.environ.get("ADMIN_EMAIL"))
print(os.environ.get("ROOT_URL"))

# Load configuration without altering the environment
print("\n\nEnv as config - ")
config = dotenv_values(shared_env_path)
pp(config)

print(os.environ.get("DOMAIN"))
print(os.environ.get("ADMIN_EMAIL"))
print(os.environ.get("ROOT_URL"))

print("\n\nEnv from .env1 file - ")
load_dotenv(curr_dir / ".env1", override=True)
print(os.environ.get("DOMAIN"))
print(os.environ.get("ADMIN_EMAIL"))
print(os.environ.get("ROOT_URL"))
