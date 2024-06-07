import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    INFERENCE_API_URL = os.environ.get("INFERENCE_API_URL")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
