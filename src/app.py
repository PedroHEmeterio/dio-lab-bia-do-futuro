import pandas as pd
import json
import request
import streamlit as st

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "gpt-oss"

perfil = json.load('(./data/perfil_investidor.json)')
transacoes = json.load('(./data/transacoes.csv)') 
historico = json.load('(./data/historico_atendimento.csv)')
produtos = json.load('(./data/produtos_financeiros.json)')

contexto = f"""
CLIENTE: {perfil['nome']}, {perfil['idade']} anos, perfil {perfil['perfil_investidor']}
OBJETIVO: {perfil['objetivo_investimento']}
PATRIMÔNIO: R$ {perfil['patrimonio_total']} | RESERVA DE EMERGÊNCIA: R$ {perfil['reserva_emergencia_atual']}

TRANSAÇÕES RECENTES:
{transacoes.to_string(index=False)}

ATENDIMENTOS ANTERIORES:
{historico.to_string(index=False)}

PRODUTOS DISPONIVEIS:
{json.dumps(produtos, indent=2, ensure_ascii=False)}
"""

SYSTEM_PROMPT = """Você é um educador de finanças focado em bolsa de valores. Seu objetivo é instruir as pessoas a entender melhor o mercado financeiro e suas regras.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos.
2. Nunca invente informações financeiras.
3. Se não souber algo, admita e ofereça alternativas.
4. Nunca recomende algum investimento.
5. Traga ao final das respostas uma pergunta para engajar o cliente a pensar em suas ações e o que fazer.
6. Crie exemplos utilizando informações do cliente e criando analogias para melhor entendimento.
7. Use linguagem simples.
"""

def perguntar(ms):
    prompt= f"""
    {SYSTEM_PROMPT}

    CONTEXTO DO CLIENTE:
    {contexto}

    Pergunta: {ms}"""

    r = request.post(OLLAMA_URL, json={"model": MODELO, "prompt": prompt, "stream": False})
    return r.json()['response']

st.title("Bem-vindo(a)! Eu sou o Invest+, seu assistente financeiro virtual.")

if pergunta := st.chat.input("Sua dúvida sobre finanças..."):
    st.chat.message("user").write(pergunta)
    with st.spinner("..."):
        st.chat.message("assistant").write(perguntar(pergunta))
