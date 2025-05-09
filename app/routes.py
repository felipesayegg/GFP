# Importa o criador de rotas e as ferramentas de dependência do FastAPI
from fastapi import APIRouter, Depends

# Importa sessão e comando "select" do SQLModel
from sqlmodel import Session, select

# Importa os modelos que vamos usar: o completo e o de criação
from app.models import Transaction, TransactionCreate

# Importa a função que fornece uma sessão com o banco
from app.database import get_session

# Cria o objeto router — é ele que vai armazenar os "caminhos" da nossa API
router = APIRouter()

@router.post("/transacoes/", response_model=Transaction)
def criar_transacao(
    transacao: TransactionCreate,
    session: Session = Depends(get_session)
):
    # Cria um novo objeto Transaction (com id vazio) a partir do que foi enviado
    nova = Transaction(**transacao.dict())

    # Adiciona a transação na sessão (ainda não foi salva no banco)
    session.add(nova)

    # Salva de verdade no banco
    session.commit()

    # Atualiza o objeto com o ID gerado pelo banco
    session.refresh(nova)

    # Retorna a transação com ID preenchido
    return nova


@router.get("/transacoes/", response_model=list[Transaction])
def listar_transacoes(session: Session = Depends(get_session)):
    # Executa um comando SELECT * FROM transaction
    transacoes = session.exec(select(Transaction)).all()

    # Retorna a lista de transações
    return transacoes


from fastapi import HTTPException

@router.delete("/transacoes/{transacao_id}")
def deletar_transacao(transacao_id: int, session: Session = Depends(get_session)):
    transacao = session.get(Transaction, transacao_id)

    # Se não encontrar a transação, retorna erro 404
    if not transacao:
        raise HTTPException(status_code=404, detail="Transação não encontrada.")

    session.delete(transacao)
    session.commit()
    return {"ok": True, "mensagem": "Transação excluída com sucesso"}
