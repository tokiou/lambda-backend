from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname
                                           (os.path.dirname(__file__))),
                           '.lambda_env')

# Cargar las variables de entorno desde el archivo .
load_dotenv(dotenv_path)
DB_HOST = os.getenv('DB-HOST')
DB_NAME = os.getenv('DB-NAME')
DB_USER = os.getenv('DB-USER')
DB_PASSWORD = os.getenv('DB-PASSWORD')
DB_PORT = os.getenv('DB-PORT')


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://" \
                          f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:" \
                          f"{DB_PORT}/{DB_NAME}"
SQLALCHEMY_DATABASE_URL_SYNC = f"postgresql://" \
                          f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:" \
                          f"{DB_PORT}/{DB_NAME}"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True,
                             future=True, echo=False)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
