import classes
import model
import requests
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from database import engine, get_db
from sqlalchemy.orm import Session
from bs4 import BeautifulSoup
from typing import List

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.post("/criar", status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)
    return {"Mensagem": mensagem_criada}

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
def busca_valores(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens

@app.get("/quadrado/{num}")
def square(num: int):
    return num ** 2

@app.get("/webscraping")
def webscraping(db: Session = Depends(get_db)):
    url_base = 'http://ufu.br/'
    resposta = requests.get(url_base)

    if resposta.status_code != 200:
        return {"Webscraping": "Falha de comunicação"}

    soup = BeautifulSoup(resposta.content, 'html.parser')
    barra_esquerda = soup.find('ul', class_='sidebar-nav nav-level-0')
    if not barra_esquerda:
        return {"Webscraping": "Elemento não encontrado"}

    linhas = barra_esquerda.find_all('li', class_='nav-item')
    resultados = []

    
    index = 0
    while index < len(linhas):
        texto = linhas[index].text.strip()
        if 'Graduação' in texto:
            break
        index += 1

    
    while index < len(linhas):
        linha = linhas[index]
        texto = linha.text.strip()

        tagLink = linha.find('a')
        tagHref = tagLink.get('href') if tagLink else None
        if tagHref:
            url_completa = url_base + tagHref.lstrip('/')
            resultados.append({
                "menuNav": texto,
                "link": url_completa
            })
        index += 1

    
    for item in resultados:
        existe = db.query(model.Model_Webscraping).filter_by(menuNav=item["menuNav"], link=item["link"]).first()
        if not existe:
            novo_registro = model.Model_Webscraping(**item)
            db.add(novo_registro)

    db.commit()
    return {"Webscraping": "Dado"}