# Importa as bibliotecas necessárias
import streamlit as st         # Para criar a interface visual
import requests                # Para se comunicar com a API
from datetime import date      # Para lidar com datas

# URL da API FastAPI (onde ela está rodando localmente)
API_URL = "http://127.0.0.1:8000"

# Configuração visual da página do Streamlit
st.set_page_config(page_title="Gerenciador Financeiro", layout="centered")

# Título principal da aplicação
st.title("💰 Gerenciador Financeiro Pessoal")

# ============================
# 💰 SALDO TOTAL (ENTRADAS - SAÍDAS)
# ============================

# Tenta buscar os dados da API para calcular o saldo
try:
    r = requests.get(f"{API_URL}/transacoes/")
    if r.status_code == 200:
        transacoes = r.json()

        # Calcula total de entradas e saídas separadamente
        total_entrada = sum(t["valor"] for t in transacoes if t["tipo"] == "entrada")
        total_saida = sum(t["valor"] for t in transacoes if t["tipo"] == "saida")
        saldo = total_entrada - total_saida

        # Mostra os valores formatados
        st.markdown(f"""
        <div style='background-color:#f0f2f6; padding:15px; border-radius:8px'>
            <h4>💵 Entradas: R$ {total_entrada:,.2f}</h4>
            <h4>💸 Saídas: R$ {total_saida:,.2f}</h4>
            <h3 style='color:{'green' if saldo >= 0 else 'red'}'>
                💰 Saldo Total: R$ {saldo:,.2f}
            </h3>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Não foi possível calcular o saldo (erro na API).")

except Exception as e:
    st.error(f"Erro ao calcular saldo: {e}")


# ============================
# 🚨 ALERTA DE LIMITE MENSAL DE GASTOS
# ============================

st.markdown("---")
st.subheader("🔔 Alerta de Limite de Gastos do Mês")

# Limite mensal pré-definido (sem input)
limite = 6000.00
st.markdown(f"💡 Limite mensal definido: **R$ {limite:,.2f}**")

# Se houver transações
if len(transacoes) > 0:
    from datetime import datetime

    hoje = datetime.today()
    # Soma somente saídas do mês atual
    gastos_mes = sum(
        t["valor"] for t in transacoes
        if t["tipo"] == "saida" and
           datetime.fromisoformat(t["data"]).month == hoje.month and
           datetime.fromisoformat(t["data"]).year == hoje.year
    )

    # Mostra quanto já foi gasto no mês
    st.info(f"Gasto atual em {hoje.strftime('%B/%Y')}: **R$ {gastos_mes:,.2f}**")

    # Alerta se estourou o limite
    if gastos_mes > limite:
        st.error(f"❌ Você ultrapassou o limite de R$ {limite:,.2f}!")
    else:
        restante = limite - gastos_mes
        st.success(f"✅ Dentro do limite. Ainda pode gastar R$ {restante:,.2f} neste mês.")


# ============================================================
# 🧾 SEÇÃO 1 — FORMULÁRIO PARA CADASTRAR NOVA TRANSAÇÃO
# ============================================================

st.subheader("📌 Nova Transação")

# Escolha do tipo de transação: entrada ou saída
tipo = st.selectbox("Tipo", ["entrada", "saida"])

# Campo de texto para o usuário digitar a categoria
categoria = st.text_input("Categoria", placeholder="Ex: salário, comida, aluguel...")

# Campo para digitar o valor em reais
valor = st.number_input("Valor (R$)", min_value=0.0, format="%.2f")

# Campo para escolher a data (padrão: hoje)
data = st.date_input("Data", value=date.today())

# Botão de envio
if st.button("Salvar Transação"):

    # Validação: campo categoria não pode estar vazio
    if categoria.strip() == "":
        st.warning("⚠️ Por favor, preencha a categoria.")

    # Validação: valor precisa ser maior que zero
    elif valor <= 0:
        st.warning("⚠️ Valor precisa ser maior que zero.")

    # Se tudo estiver preenchido corretamente, envia pra API
    else:
        # Monta os dados num dicionário
        payload = {
            "tipo": tipo,
            "categoria": categoria,
            "valor": valor,
            "data": str(data)  # converte data para string no formato "YYYY-MM-DD"
        }

        # Tenta fazer o POST para a API
        try:
            r = requests.post(f"{API_URL}/transacoes/", json=payload)

            # Se deu certo (HTTP 200 OK), mostra sucesso
            if r.status_code == 200:
                st.success("✅ Transação salva com sucesso!")

            # Se não deu certo, mostra erro genérico
            else:
                st.error("❌ Erro ao salvar a transação.")

        # Se deu erro na conexão (API não está rodando, por exemplo)
        except Exception as e:
            st.error(f"Erro ao conectar com a API: {e}")

# Linha divisória visual
st.markdown("---")

# ============================================================
# ============================
# 📋 LISTAGEM COM BOTÃO EXCLUIR
# ============================

st.markdown("---")
st.subheader("📄 Histórico de Transações")

try:
    r = requests.get(f"{API_URL}/transacoes/")
    if r.status_code == 200:
        transacoes = r.json()

        if len(transacoes) == 0:
            st.info("Nenhuma transação cadastrada ainda.")
        else:
            for t in transacoes:
                col1, col2, col3 = st.columns([6, 2, 2])  # layout da linha

                with col1:
                    st.markdown(
                        f"📌 **{t['categoria']}** | 💸 R$ {t['valor']:.2f} | 📅 {t['data']} | 🔖 *{t['tipo']}*"
                    )

                with col2:
                    if st.button("❌ Excluir", key=f"del_{t['id']}"):
                        try:
                            del_req = requests.delete(f"{API_URL}/transacoes/{t['id']}")
                            if del_req.status_code == 200:
                                st.success("Transação excluída!")
                                st.experimental_rerun()  # recarrega a página
                            else:
                                st.error("Erro ao excluir.")
                        except Exception as e:
                            st.error(f"Erro na conexão: {e}")
    else:
        st.error("Erro ao buscar transações.")
except Exception as e:
    st.error(f"Erro ao conectar com a API: {e}")
