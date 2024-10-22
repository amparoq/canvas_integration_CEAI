from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

USER = 'amparo'
PASSWORD = '1234'
HOST = 'localhost'
DATABASE = 'canvas_test'
LLAVE = b'_5#y2L"F4Q8z\n\xec]/'


engine = create_engine(
    f'mysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}',
    pool_recycle=3600,
    pool_pre_ping=True
)

# Crea una instancia de Session.
Session = sessionmaker(bind=engine)
session = Session()


# Función para obtener la instancia de la sesión.
def get_session():
    return session