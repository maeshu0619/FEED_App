import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.environ.get("DB_DIR", os.path.join(BASE_DIR, "data"))  # ← data/ は作成される前提
os.makedirs(DB_DIR, exist_ok=True)  # ← これが重要（起動時に確実に作る）
class Config:
    DB_PATH = os.path.join(DB_DIR, "dogfeed.db")
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
