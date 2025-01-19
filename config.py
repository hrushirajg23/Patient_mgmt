from typing import List
from pydantic import BaseSettings
import sys
from pathlib import Path


class Settings(BaseSettings):
    SERVER: str
    db_host: str
    db_port: int
    db_name: str
    db_pwd: str
    db_usr: str

    

    class Config:
        env_file = Path(Path(__file__).resolve().parent) / ".env"
        print("server started successfully!!")


setting = Settings()
