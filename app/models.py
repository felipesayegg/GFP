from sqlmodel import SQLModel, Field
from datetime import date
from typing import Optional

# Modelo principal: representa uma transação no banco (entrada ou saída)
class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # ID gerado automaticamente
    tipo: str            # pode ser "entrada" ou "saida"
    categoria: str       # ex: alimentação, salário, transporte
    valor: float         # valor em reais
    data: date           # data da transação

# Modelo auxiliar: usado só para criar uma nova transação (sem precisar informar o ID)
class TransactionCreate(SQLModel):
    tipo: str
    categoria: str
    valor: float
    data: date