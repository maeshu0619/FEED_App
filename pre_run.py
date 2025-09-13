import os

# 一時的に直書き（実際の値を入れてください）
os.environ["DATABASE_URL"] = "postgresql://USERNAME:PASSWORD@HOST:PORT/DBNAME"

from app import create_app, db
from app.models import Feed, Trash

app = create_app()
with app.app_context():
    db.create_all()
