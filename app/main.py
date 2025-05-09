# Importa o FastAPI (framework principal da API)
from fastapi import FastAPI

# Importa a função que cria o banco de dados
from app.database import create_db

# Importa as rotas já organizadas no arquivo routes.py
from app.routes import router as finance_router

# Cria a aplicação FastAPI — isso é o coração da sua API
app = FastAPI(title="Gerenciador Financeiro Pessoal")

# Toda vez que a API iniciar, essa função será chamada automaticamente
# Aqui a gente garante que as tabelas do banco serão criadas, caso não existam
@app.on_event("startup")
def startup():
    create_db()

# Aqui a gente conecta todas as rotas da API (endpoints) definidas em routes.py
# Isso evita deixar tudo no main.py e mantém o projeto organizado
app.include_router(finance_router)
