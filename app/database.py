# Importa as ferramentas da SQLModel para trabalhar com banco de dados
from sqlmodel import SQLModel, create_engine, Session

# Define o caminho do banco de dados SQLite
# "sqlite:///./finance.db" significa:
# - estamos usando o banco SQLite
# - o arquivo do banco vai ser criado na raiz do projeto como "finance.db"
DATABASE_URL = "sqlite:///./finance.db"

# Cria o "engine", que é o motor de conexão com o banco de dados
# É ele que o Python usa por trás pra se comunicar com o banco
# echo=True faz mostrar os comandos SQL no terminal (bom pra ver o que está acontecendo)
engine = create_engine(DATABASE_URL, echo=True)

# Função que cria todas as tabelas do banco de dados, com base nos modelos definidos com "table=True"
def create_db():
    SQLModel.metadata.create_all(engine)
    # Essa linha lê todos os modelos (ex: Transaction) e cria as tabelas no banco
    # Se o banco já existir, não cria de novo — é seguro rodar várias vezes

# Função que abre uma conexão com o banco de dados
# É usada nos endpoints da API para acessar e modificar os dados
def get_session():
    with Session(engine) as session:
        yield session
        # "yield" funciona como um "retorna temporário"
        # Ele entrega a sessão pra quem pediu (ex: rota de cadastro ou listagem)
        # Quando acabar de usar, a sessão é fechada automaticamente com o "with"
