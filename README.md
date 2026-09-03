# Finantivo

Protótipo de agente de IA financeiro, desenvolvido como projeto final do bootcamp **DIO + Bradesco**, a partir da base [`dio-lab-bia-do-futuro`](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).

O Finantivo vai além de responder perguntas sobre saldo, produtos e histórico de transações: ele **analisa o comportamento financeiro do cliente para antecipar tendências de gastos**, gera alertas quando identifica desvios de padrão e recomenda produtos financeiros compatíveis com o perfil de cada cliente — em vez de só reagir ao que é perguntado.

## O que é o projeto

Um agente conversacional que combina três coisas:

1. **Dados financeiros mockados** de um cliente (transações, perfil de investidor, catálogo de produtos, histórico de atendimento);
2. **Uma camada de análise estatística** que processa esses dados antes de qualquer resposta — calculando gasto por categoria, variação em relação à média histórica e projeção de fechamento do mês;
3. **Um LLM (Google Gemini)**, que recebe esse contexto já processado e conversa com o cliente em linguagem natural, respeitando um conjunto de regras e um tom consultivo definidos via prompt engineering.

## Como funciona

```
Usuário digita uma pergunta no terminal
            │
            ▼
   app.py carrega os dados mockados (data/)
            │
            ▼
   analytics.py processa os dados:
   - gasto por categoria no mês atual
   - média dos últimos 3 meses fechados
   - variação percentual e alertas (limite: >20%)
   - projeção de fechamento do mês (extrapolação linear)
            │
            ▼
   app.py monta o contexto (perfil + resumo financeiro +
   produtos compatíveis com o perfil de risco do cliente)
            │
            ▼
   app.py envia para o Gemini:
   - system prompt (prompts.py)
   - few-shot examples (prompts.py)
   - contexto + pergunta do usuário
            │
            ▼
   Resposta em linguagem natural exibida no terminal
```

A análise da camada preditiva é **estatística clássica** (extrapolação linear e comparação com média histórica), uma escolha deliberada para o volume de dados de um protótipo, priorizando explicabilidade. Essa decisão está detalhada em `Docs/02-base-conhecimento.md`.

## Funcionalidades

- **Consulta de dados**: transações, perfil de investidor e catálogo de produtos;
- **Análise de tendência**: gasto por categoria comparado à média dos últimos 3 meses fechados;
- **Projeção de fechamento do mês**: estimativa de gasto total com base no ritmo de gastos até a data de referência;
- **Alertas automáticos**: quando uma categoria varia mais de 20% em relação à média, o agente é instruído a trazer isso proativamente na conversa;
- **Recomendação contextual de produtos**: o catálogo é filtrado pelo perfil de risco do cliente antes de chegar ao LLM, então o agente só sugere produtos compatíveis;
- **Guardrails de conversa**: recusa educada para perguntas fora do escopo financeiro, e para pedidos de dados sensíveis (senhas, dados de outros clientes) — definidos em `Src/Prompts.py`;
- **Resiliência a falhas de API**: retry automático com backoff exponencial para erros transitórios (sobrecarga do servidor, falha de conexão), em vez de encerrar o programa.

## Tecnologias

| Tecnologia | Uso |
|---|---|
| **Python 3.12** | Linguagem principal |
| **pandas** | Processamento dos dados de transações (agregação, cálculo de variação e projeção) |
| **Google Gemini API** (`google-genai`, modelo `gemini-3.6-flash`) | Modelo de linguagem que conversa com o usuário |
| **python-dotenv** | Carregamento da chave de API a partir de um arquivo `.env` local (nunca commitado) |

## Como roda atualmente

Hoje a aplicação roda via **terminal** (interface Streamlit ainda não implementada — ver Roadmap).

```bash
# 1. Clonar o repositório
git clone https://github.com/GiovanniZucolin/agente-financeiro-preditivo.git
cd agente-financeiro-preditivo

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Configurar a chave da API
# Copie .env.example para .env e cole sua chave do Gemini
# (gere uma gratuita em https://aistudio.google.com/app/apikey)

# 4. Rodar o agente (a partir da raiz do projeto)
python Src/app.py
```

O programa abre um loop de conversa no terminal — digite sua pergunta, receba a resposta, e digite `sair` para encerrar.

## Estrutura do repositório

```
agente-financeiro-preditivo/
├── .env                    # chave da API (NÃO commitado - protegido pelo .gitignore)
├── .env.example             # template do .env, para quem clonar o projeto
├── .gitignore
├── README.md
├── requirements.txt
├── gerar_dados.py            # script que gera os dados mockados de Data/
├── Assets/                   # recursos de apoio do projeto
├── Data/                     # dados mockados do cliente
│   ├── transacoes.csv
│   ├── perfil_investidor.json
│   ├── produtos_financeiros.json
│   └── historico_atendimento.csv
├── Docs/                      # documentação do projeto (fase de concepção)
│   ├── 01-documentacao-agente.md    # caso de uso e arquitetura
│   ├── 02-base-conhecimento.md      # estratégia de dados
│   ├── 03-prompts.md                # engenharia de prompts
│   ├── 04-metricas.md               # avaliação e métricas
│   └── 05-pitch.md                  # roteiro do pitch
└── Src/                        # código da aplicação
    ├── app.py                  # orquestrador: carrega dados, chama analytics, monta contexto, chama o Gemini
    ├── Analytics.py             # camada de análise preditiva (função pura, sem dependência de LLM/interface)
    └── Prompts.py                # system prompt, few-shot examples e guardrails
```

## Status do projeto

### 🚧 Próximos passos

- [ ] Ajustar os dados mockados para que o alerta de tendência dispare de forma mais evidente na demo (hoje a baseline dos últimos 3 meses está parcialmente contaminada pelo próprio pico de gastos simulado)
- [ ] Construir a interface em Streamlit, substituindo o loop de terminal atual
- [ ] Rodar a bateria de testes descrita em `Docs/04-metricas.md` e preencher a tabela de resultados
