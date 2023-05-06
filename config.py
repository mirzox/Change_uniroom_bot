import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    API_TOKEN = os.environ.get('API_TOKEN')
    ADMIN_ID = os.environ.get('ADMIN_ID')
    GROUP_ID = os.environ.get('GROUP_ID')