# 05. Roteiro do Pitch

> Duração alvo: 5 a 7 minutos. Estrutura pensada para prender atenção logo no início com o problema, e fechar com o diferencial técnico.

## 1. Abertura — Gancho (30s)

> "Hoje, um assistente financeiro só te responde quando você pergunta. Ele nunca te avisa antes que algo aconteça. E se ele pudesse perceber, antes de você, que seus gastos estão saindo do padrão — e já te sugerir o que fazer a respeito?"

## 2. O Problema (1 min)

- Assistentes financeiros tradicionais são **reativos**: só agem quando o cliente pergunta;
- O cliente descobre desvios no orçamento tarde demais — no fim do mês, ou no extrato;
- O banco tem o histórico de transações do cliente, mas raramente o transforma em algo proativo e personalizado na conversa do dia a dia.

## 3. A Solução — BIA Preditiva (1 min)

- Um agente financeiro que não só responde, mas **analisa o histórico de transações** do cliente em tempo real;
- Identifica tendências (ex: "gastos com alimentação 32% acima da média");
- Projeta o fechamento do mês;
- Recomenda produtos financeiros no momento certo, com base no comportamento observado — não só no que o cliente perguntou.

## 4. Demonstração (2–3 min)

Roteiro sugerido para a demo ao vivo:

1. Iniciar a conversa como um cliente comum: perguntar o saldo/gastos do mês;
2. Mostrar o agente trazendo um **alerta proativo** sobre uma categoria de gasto fora do padrão;
3. Perguntar "vale a pena investir algo esse mês?" e mostrar a **recomendação contextualizada**, citando a projeção de saldo como motivo;
4. (Opcional) Mostrar um caso de guardrail — perguntar algo fora de escopo (ex: previsão do tempo) e mostrar a recusa educada.

## 5. Diferencial Técnico (1 min)

- Camada de **pré-processamento analítico** roda antes do LLM: o modelo recebe insights já calculados, não dados brutos — isso reduz alucinação de números;
- Prompt estruturado com **regras explícitas + few-shot examples**, garantindo tom consultivo e comportamento seguro;
- Arquitetura pensada para evoluir: hoje usa dados mockados e injeção direta de contexto; o desenho já prevê migração para RAG e dados em tempo real.

## 6. Resultados / Aprendizados (30s)

- O que funcionou bem nos testes;
- Principais desafios encontrados (ex: calibrar o limiar de alerta para não gerar ruído excessivo);
- O que ficou claro sobre engenharia de prompt para reduzir alucinação.

## 7. Próximos Passos (30s)

- Conectar a dados reais (API bancária) em vez de mocks;
- Adicionar modelo preditivo mais robusto (ex: séries temporais) conforme o histórico de dados cresça;
- Personalizar o limiar de alerta por cliente (o que é "normal" varia de pessoa para pessoa);
- Adicionar canal de feedback do usuário para medir utilidade das recomendações.

## 8. Fechamento

> "A diferença entre um chatbot e um copiloto financeiro é simples: um espera a pergunta, o outro já viu o problema antes de você perguntar. É isso que a BIA Preditiva propõe."

---

### Checklist antes da apresentação
- [ ] Testar a demo com os 3 fluxos (consulta, alerta, recomendação) sem falhas
- [ ] Ter um cenário de fallback caso a API do LLM falhe ao vivo (print/vídeo gravado)
- [ ] Cronometrar o pitch pelo menos uma vez
- [ ] Preparar resposta para a pergunta mais provável: "como vocês evitam que o modelo alucine números?"
