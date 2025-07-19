from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, String, text
from sqlalchemy.sql import text 
from database import Base

class Model_Mensagem(Base):
    __tablename__ = "Mensagem"


    id = Column(Integer, primary_key=True, nullable=False)
    titulo = Column(String, nullable=False)
    conteudo = Column(String, nullable=False)
    publicada = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Model_Webscraping(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, nullable=False)
    menuNav = Column(String, nullable=False)
    link = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
