import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # プロジェクト直下に dogfeed.db を置く
    DB_PATH = os.path.join(BASE_DIR, "dogfeed.db")
    SECRET_KEY = "change-this-in-production"
