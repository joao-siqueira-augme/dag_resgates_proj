from sqlmodel import create_engine
from url_banco import UrlBanco

url_risco = UrlBanco(name_db="Risco").SQLALCHEMY_DATABASE_URI

engine_risco = create_engine(
    url=url_risco,
    echo=False
)