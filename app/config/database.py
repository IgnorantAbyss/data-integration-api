# app/config/database.py

# create_engine:
# - SQLAlchemy 用來建立資料庫引擎的函式。
# -「程式要透過哪個入口連去資料庫」。
from sqlalchemy import create_engine

# declarative_base:
# - 建立 ORM model 的共同父類別 Base。
# - ORM class 繼承 Base。
from sqlalchemy.orm import declarative_base

# sessionmaker:
# - 用來建立 Session
# - 用 SessionLocal() 產生真正的 session 物件。
from sqlalchemy.orm import sessionmaker

import urllib

from app.config.config import Settings

setting = Settings()

# DATABASE_URL:
# - SQLAlchemy 連線字串。
odbc_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={setting.sql_url};"
    "DATABASE=TFB_gcti_ivr_eos;"
    f"UID={setting.sql_acc};"
    f"PWD={setting.sql_password};"
    "TrustServerCertificate=yes;"
)

DATABASE_URL = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(odbc_str)

# - 建立資料庫引擎。
engine = create_engine(DATABASE_URL)

# SessionLocal:
# - 這是一個 Session 工廠，不是 session 本身。
# - 真正使用時要寫 SessionLocal() 才會產生 db session。
# - autocommit=False:
#   不會自動 commit，要你自己明確 db.commit()，比較安全。
# - autoflush=False:
#   不會在你查詢或其他時機自動把暫存資料送到 DB。
# - bind=engine:
#   表示這個 Session 工廠所產生的 session，都要綁到這個 engine。
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base:
# - 所有 ORM model 的共同父類別。
Base = declarative_base()

def get_db():
    # get_db:
    # - 給 FastAPI 用的 dependency function。
    # - 每次 API 請求進來時，建立一個 session，
    #   用完後自動 close。
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()