"""
app.py

Orquestrador do Finantivo.

Responsabilidade: carregar os dados, acionar a camada de análise preditiva
(analytics.py), montar o contexto completo e enviar para o LLM e exibir a resposta na interface.

Este arquivo não deve conter lógica de cálculo (isso é papel do
analytics.py) nem texto de prompt (isso é papel do prompts.py) - só orquestra.
"""

import json
import os
import time

import pandas as pd
from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors
from google.genai import types

from Analytics import calcular_resumo_financeiro
from Prompts import SYSTEM_PROMPT, FEW_SHOT_EXAMPLES

# Carrega variáveis do arquivo .env (se existir) para o ambiente do processo.
# Assim GEMINI_API_KEY não precisa ser digitada manualmente no terminal toda vez
load_dotenv()

MODELO_GEMINI = "gemini-3.6-flash"


def carregar_dados():
    """Carrega os dados mockados do cliente a partir de data/."""
    with open("./data/perfil_investidor.json", "r", encoding="utf-8") as f:
        perfil = json.load(f)

    transacoes = pd.read_csv("./data/transacoes.csv")
    historico = pd.read_csv("./data/historico_atendimento.csv")

    with open("./data/produtos_financeiros.json", "r", encoding="utf-8") as f:
        produtos = json.load(f)

    return perfil, transacoes, historico, produtos


def filtrar_produtos_compativeis(produtos: list, perfil: dict) -> list:
    """Filtra o catálogo de produtos pelos compatíveis com o perfil de risco do cliente."""
    perfil_risco = perfil.get("perfil_risco")
    return [
        produto
        for produto in produtos
        if perfil_risco in produto.get("perfis_compativeis", [])
    ]


def montar_contexto(perfil: dict, resumo_financeiro: dict, produtos_compativeis: list) -> dict:
    """Monta o dicionário de contexto completo que será enviado ao LLM."""
    return {
        "perfil_investidor": perfil,
        "resumo_financeiro": resumo_financeiro,
        "produtos_compativeis": produtos_compativeis,
        # TODO: incluir trechos relevantes de "historico" quando a lógica de
        # continuidade de atendimento (ex: "você já perguntou algo parecido
        # antes") for implementada.
    }


def montar_historico_few_shot() -> list:
    """ Converte FEW_SHOT_EXAMPLES (definidos em prompts.py) para o formato de 
    histórico de turnos que o Gemini espera: uma lista alternando role="user" e role="model". """
    
    historico = []
    for exemplo in FEW_SHOT_EXAMPLES:
        if exemplo["usuario"] is None:
            continue
        historico.append({"role": "user", "parts": [{"text": exemplo["usuario"]}]})
        historico.append({"role": "model", "parts": [{"text": exemplo["Finantivo"]}]})
    return historico


def montar_mensagem_usuario(contexto: str, pergunta: str) -> str:
    """Combina o contexto de dados do cliente com a pergunta feita, numa única mensagem de usuário."""
    return (
        f"[CONTEXTO DO CLIENTE]\n{contexto}\n\n"
        f"[PERGUNTA DO CLIENTE]\n{pergunta}"
    )


def chamar_llm(contexto: str, pergunta: str, max_tentativas: int = 3) -> str:
    """
    Envia a pergunta do usuário para o Gemini, junto com o system prompt,
    os few-shot examples e o contexto de dados do cliente.

    Requer a variável de ambiente GEMINI_API_KEY configurada
    """
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "Variável de ambiente GEMINI_API_KEY não encontrada. "
            "Gere uma chave gratuita em https://aistudio.google.com/app/apikey "
            "e configure antes de rodar."
        )

    client = genai.Client()

    historico = montar_historico_few_shot()
    mensagem_usuario = montar_mensagem_usuario(contexto, pergunta)
    conteudo_final = historico + [{"role": "user", "parts": [{"text": mensagem_usuario}]}]

    for tentativa in range(1, max_tentativas + 1):
        try:
            resposta = client.models.generate_content(
                model=MODELO_GEMINI,
                contents=conteudo_final,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            )
            return resposta.text
        except genai_errors.ServerError:
            if tentativa == max_tentativas:
                raise RuntimeError(
                    "O Gemini está temporariamente sobrecarregado (erro 503) "
                    "e não respondeu após várias tentativas. Tente de novo "
                    "em alguns instantes."
                )
            espera = 2 ** tentativa  # backoff exponencial: 2s, 4s, 8s...
            print(f"[Servidor sobrecarregado, tentando novamente em {espera}s...]")
            time.sleep(espera)

    return resposta.text


def main():
    perfil, transacoes, historico, produtos = carregar_dados()

    resumo_financeiro = calcular_resumo_financeiro(transacoes)
    produtos_compativeis = filtrar_produtos_compativeis(produtos, perfil)

    contexto_dict = montar_contexto(perfil, resumo_financeiro, produtos_compativeis)
    contexto = json.dumps(contexto_dict, ensure_ascii=False, indent=2)

    # Loop simples de conversa via terminal
    # com o LLM antes de construir a interface (Streamlit) de verdade.
    print("Finantivo - digite sua pergunta (ou 'sair' para encerrar)\n")
    while True:
        pergunta = input("Você: ").strip()
        if pergunta.lower() in ("sair", "exit", "quit"):
            break
        try:
            resposta = chamar_llm(contexto, pergunta)
            print(f"\nFinantivo: {resposta}\n")
        except RuntimeError as erro:
            print(f"\n[Erro: {erro}]\n")


if __name__ == "__main__":
    main()