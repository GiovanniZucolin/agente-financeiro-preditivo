# 02. Base de Conhecimento — Estratégia de Dados

## 1. Fontes de Dados

| Arquivo | Tipo | Conteúdo | Uso pelo agente |
|---|---|---|---|
| `transacoes.csv` | Estruturado | Histórico de transações do cliente (data, categoria, valor, tipo) | Base para consultas diretas **e** para a camada preditiva |
| `perfil_investidor.json` | Estruturado | Perfil de risco, objetivos e características do cliente | Contextualiza recomendações e tom das respostas |
| `produtos_financeiros.json` | Estruturado | Catálogo de produtos disponíveis (renda fixa, fundos, cartões, etc.) | Base para recomendações |
| `historico_atendimento.csv` | Estruturado | Interações anteriores do cliente com o banco | Contexto de continuidade ("você já perguntou algo parecido antes") |

## 2. Estratégia de Acesso aos Dados

Como o volume de dados mockados é pequeno e estruturado (não é texto livre), **não é necessário RAG com embeddings/vetorização** para esta versão do protótipo. A estratégia adotada é **injeção direta de contexto estruturado** no prompt:

1. Os dados relevantes ao cliente ativo são carregados a cada interação;
2. São filtrados/agregados conforme a pergunta (ex: apenas transações do último trimestre);
3. São formatados em um bloco de contexto (JSON ou texto tabular resumido) e inseridos no prompt enviado ao LLM.

> Nota para evolução futura: caso a base cresça (ex: milhares de transações, textos de atendimento longos), a estratégia deve migrar para RAG com busca vetorial (embeddings + vector store), pois a injeção direta deixa de ser viável pelo limite de contexto do modelo.

## 3. Camada de Pré-processamento (Analytics)

Esta é a camada que diferencia a BIA Preditiva do agente base. Antes de qualquer chamada ao LLM, o sistema executa:

1. **Agregação por categoria e período** — soma de gastos por categoria, agrupados por mês;
2. **Cálculo de variação** — comparação percentual entre o mês corrente e a média dos últimos 3 meses;
3. **Projeção simples** — média móvel (ou regressão linear simples) para estimar o gasto total do mês corrente com base no ritmo observado até a data;
4. **Geração de alertas** — regras simples que classificam a variação:
   - Variação > +20% em uma categoria → alerta de "gasto elevado";
   - Saldo projetado positivo relevante → gatilho de "oportunidade de investimento";
   - Variação dentro do normal → sem alerta.

Essas informações processadas (não os dados brutos) são o que entra no prompt como "insights", reduzindo a chance de o LLM ter que fazer contas sozinho (e alucinar números).

## 4. Estrutura do Contexto Enviado ao LLM

Exemplo de bloco de contexto montado dinamicamente antes de cada chamada:

```json
{
  "perfil_investidor": { "...": "..." },
  "resumo_financeiro": {
    "gasto_total_mes_atual": 3200.00,
    "categorias": [
      { "categoria": "Alimentação", "gasto_mes_atual": 850.00, "variacao_percentual": 32.0 },
      { "categoria": "Transporte", "gasto_mes_atual": 400.00, "variacao_percentual": -5.0 }
    ],
    "projecao_fim_mes": 3900.00,
    "alertas": ["Gasto com Alimentação 32% acima da média dos últimos 3 meses"]
  },
  "produtos_compativeis": [ "...lista filtrada pelo perfil..." ]
}
```

## 5. Manutenção e Atualização da Base

- Para o protótipo, os dados são estáticos (arquivos mockados versionados no repositório);
- Em uma evolução real, `transacoes.csv` seria substituído por uma consulta a um banco de dados/API transacional em tempo real;
- O catálogo de produtos (`produtos_financeiros.json`) deveria ter uma rotina de atualização periódica, já que produtos financeiros mudam (taxas, condições).

## 6. Limitações Conhecidas da Base Atual

- Dados mockados representam um único cliente por vez (sem multi-tenant real);
- Sem histórico longo o suficiente para modelos preditivos sofisticados — por isso a escolha por método estatístico simples (média móvel) em vez de ML complexo;
- Sem dados de mercado externos (CDI, inflação) que enriqueceriam a recomendação.
