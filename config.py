import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ADMIN_KEY = os.environ.get("ADMIN_KEY")
    INFERENCE_API_URL = os.environ.get("INFERENCE_API_URL")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
if __name__ == "__main__":
    print(Config.SECRET_KEY)
    print(Config.INFERENCE_API_URL)
    print(Config.SQLALCHEMY_DATABASE_URI)
    print(Config.SQLALCHEMY_TRACK_MODIFICATIONS)