from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables or a .env file.
    Purpose:
        Centralize config values so other modules do not hard-code paths or
        provider-specific settings.
    """

    Txnip: str
    secret : str
    sql_url : str
    sql_acc : str
    sql_password : str

    # 新版 pydantic-settings 推薦用這個設定
    model_config = SettingsConfigDict(
        env_file=".env",              # 指定要讀取的 .env 檔案
        env_file_encoding="utf-8",    # 指定 .env 編碼
        case_sensitive=False          # 環境變數名稱是否大小寫敏感
    )
