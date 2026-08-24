# Finantivo - Assistente Financeiro Preditivo

Protótipo de agente de IA financeiro desenvolvido como projeto final do bootcamp **DIO + Bradesco**, a partir da base [`dio-lab-bia-do-futuro`](https://github.com/digitalinnovationone/dio-lab-bia-do-futuro).

O Finantivo - Assistente Financeiro Preditivo vai além de responder perguntas sobre saldo, produtos e histórico de transações: ela **analisa o comportamento financeiro do cliente para antecipar tendências de gastos**, gerar alertas proativos e recomendar produtos financeiros no momento certo — em vez de só reagir ao que é perguntado.

> 📄 Documentação completa do conceito, arquitetura, prompts, métricas e pitch em [`docs/`](./docs).

## Status do projeto

Este é um projeto em desenvolvimento. Abaixo, o que já foi feito e o que ainda falta.

### ✅ Feito

- [x] Definição do conceito e diferencial do agente (saúde financeira preditiva + recomendação contextual de produtos)
- [x] Documentação de caso de uso e arquitetura (`docs/01-documentacao-agente.md`)
- [x] Documentação da estratégia de dados e camada de pré-processamento analítico (`docs/02-base-conhecimento.md`)
- [x] Engenharia de prompts — system prompt, few-shot examples e guardrails (`docs/03-prompts.md`)
- [x] Definição de métricas de avaliação (qualidade do LLM, camada preditiva e produto) (`docs/04-metricas.md`)
- [x] Roteiro de pitch com script de demonstração (`docs/05-pitch.md`)
- [x] Script de geração dos dados mockados (`gerar_dados.py`), expandindo a base original com mais colunas e ~6 meses de histórico, incluindo uma tendência proposital de gastos para viabilizar a demo de alerta preditivo
- [x] Gerado os arquivos finais em `data/` (`transacoes.csv`, `perfil_investidor.json`, `produtos_financeiros.json`, `historico_atendimento.csv`)

### 🚧 Em andamento / próximos passos

- [ ] Implementar a camada de análise preditiva (`src/analytics.py`): agregação por categoria/mês, cálculo de variação, projeção de fechamento do mês e geração de alertas
- [ ] Implementar o orquestrador e a interface (`src/app.py`), integrando dados + camada preditiva + chamada ao LLM
- [ ] Testar os fluxos de conversa definidos nos casos de uso (consulta, alerta proativo, recomendação, guardrails)
- [ ] Rodar a bateria de testes descrita em `docs/04-metricas.md` e preencher a tabela de resultados

## Estrutura do repositório

```
bia-preditiva/
├── README.md
├── data/                           # dados mockados do cliente (a gerar)
│   ├── transacoes.csv
│   ├── perfil_investidor.json
│   ├── produtos_financeiros.json
│   └── historico_atendimento.csv
├── docs/                           # documentação do projeto
│   ├── 01-documentacao-agente.md   # caso de uso e arquitetura
│   ├── 02-base-conhecimento.md     # estratégia de dados
│   ├── 03-prompts.md               # engenharia de prompts
│   ├── 04-metricas.md              # avaliação e métricas
│   └── 05-pitch.md                 # roteiro do pitch
├── src/                            # código da aplicação (em desenvolvimento)
│   ├── app.py                      # orquestrador + interface
│   └── analytics.py                # camada de análise preditiva
└── gerar_dados.py                  # script de geração dos dados mockados
```
