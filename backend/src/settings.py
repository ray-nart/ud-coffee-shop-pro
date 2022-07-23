import os
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')
DB_FILE_NAME = os.environ.get('DB_FILE_NAME')
