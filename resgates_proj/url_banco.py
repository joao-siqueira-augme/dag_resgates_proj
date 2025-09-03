from pydantic import computed_field
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv('DB_DRIVER')
DB_DRIVER_NAME = os.getenv('DB_DRIVER_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD_RISCO = os.getenv('DB_PASSWORD_RISCO')
DB_PORT = os.getenv('DB_PORT')
DB_USER_RISCO = os.getenv('DB_USER_RISCO')


class UrlBanco():
    def __init__(self, name_db: str = None):
        self.db_driver_name = DB_DRIVER_NAME
        self.db_host = DB_HOST
        self.db_port= DB_PORT
        self.db_user = DB_USER_RISCO
        self.db_password = DB_PASSWORD_RISCO
        self.db_name = name_db
        self.db_driver= DB_DRIVER

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> URL:
        return (
            f"{self.db_driver_name}://"
            f"{self.db_user}:"
            f"{self.db_password}@"
            f"{self.db_host}:"
            f"{self.db_port}/"
            f"{self.db_name}?"
            f"driver={self.db_driver}"
        )