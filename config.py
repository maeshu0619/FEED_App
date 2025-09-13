import os

uri = os.environ.get("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    # psycopg3 用のドライバ指定に書き換える
    uri = uri.replace("postgres://", "postgresql+psycopg://", 1)
elif uri and uri.startswith("postgresql://"):
    uri = uri.replace("postgresql://", "postgresql+psycopg://", 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False


# import os

# class Config:
#     # Render の Environment に保存した DATABASE_URL を参照
#     SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SECRET_KEY = os.environ.get("SECRET_KEY", "change-me")
