import json
import pandas as pd

#Carregar os dados

with open('./data/perfil_investidor.json', 'r', encoding='utf-8') as f:
    perfil = json.load(f)
transacoes = pd.read_csv('./data/transacoes.csv')
historico = pd.read_csv('./data/historico_atendimento.csv')
with open('./data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
    produtos = json.load(f)

# Procesasndo os dados para o Agente

transacoes['data'] = pd.to_datetime(transacoes['data'])

data_atual = transacoes['data'].max()       # <- Para dados mockados / pd.Timestamp.now() -> Para dados dinâmicos
ano_atual = data_atual.year
mes_atual = data_atual.month
dia_atual = data_atual.day
ultimo_dia = data_atual.to_period('M').end_time.day
inicio_mes = data_atual.to_period('M').to_timestamp()
inicio_3mes = data_atual.to_period('M').to_timestamp() - pd.DateOffset(months=3)

#                   Gasto Total do Mês Atual
categorias_mes_atual = transacoes[
    (transacoes["data"] >= inicio_mes) &
    (transacoes["data"] <= data_atual) &
    (transacoes["tipo"] == 'debito')
]

gasto_total_mes_atual = categorias_mes_atual['valor'].sum()

#                   Categorias
# Gastos do mês atual

total_atual = categorias_mes_atual.groupby("categoria")["valor"].sum()

# Gastos dos 3 meses anteriores
categorias_3meses = transacoes[
    (transacoes["data"] >= inicio_3mes) &
    (transacoes["data"] < inicio_mes) &
    (transacoes["tipo"] == 'debito')
]

totais_3meses = categorias_3meses.groupby(
    [categorias_3meses["data"].dt.to_period("M"), "categoria"]
)["valor"].sum().reset_index()

# Média mensal dos últimos 3 meses, por categoria
media_categorias_3meses = totais_3meses.groupby(
    "categoria"
)["valor"].mean()

# Variação percentual do mês atual em relação à média
variacao_media_categoria = (
    (total_atual - media_categorias_3meses)
    / media_categorias_3meses
) * 100

resumo_categorias = pd.DataFrame({
    "gasto_atual": round(total_atual,2),
    "media_3_meses": round(media_categorias_3meses,2),
    "variacao_%": round(variacao_media_categoria,2)
}).reset_index()
# Categorias que só existem em um dos dois períodos (ex: categoria nova, sem histórico nos últimos 3 meses) geram NaN na subtração/divisão.
# NaN não é um valor JSON válido, então removemos essas linhas do resumo (elas não têm uma "média" confiável pra comparar de qualquer forma).
resumo_categorias = resumo_categorias.dropna(subset=["gasto_atual", "media_3_meses", "variacao_%"])

lista_json = resumo_categorias.to_dict(orient="records")

#               Calcula a orijeção até o fim do mês
gasto_medio_diario = gasto_total_mes_atual / dia_atual
projecao_fim_mes = gasto_medio_diario * ultimo_dia

#               Gera Alertas
alertas = resumo_categorias[
    resumo_categorias["variacao_%"] > 20
].apply(
    lambda linha: f"Gasto com {linha['categoria']} "
                  f"{linha['variacao_%']:.2f}% acima da média dos últimos 3 meses",
    axis=1
).tolist()


#           Fornencendo as informações pro Agente
contexto_dict = {
    "perfil_investidor": perfil,
    "resumo_financeiro": {
        "gasto_total_mes_atual": round(gasto_total_mes_atual, 2),
        "categorias": lista_json,
        "projecao_fim_mes": round(projecao_fim_mes, 2),
        "alertas": alertas
    }
}

contexto = json.dumps(contexto_dict, ensure_ascii=False, indent=2)

print(contexto)