# 04. Avaliação e Métricas

## 1. Objetivo da Avaliação

Garantir que a BIA Preditiva responda com precisão sobre os dados do cliente, gere alertas/projeções coerentes com os dados reais (mockados) e mantenha um comportamento seguro dentro do escopo definido.

## 2. Métricas de Qualidade da Resposta (LLM)

| Métrica | O que mede | Como medir |
|---|---|---|
| **Aderência aos dados (Groundedness)** | Se a resposta usa apenas informações presentes no contexto fornecido | Revisão manual de uma amostra de conversas comparando resposta x dados de entrada |
| **Taxa de alucinação** | Frequência com que o agente inventa números, produtos ou transações inexistentes | Testes com perguntas cuja resposta correta é conhecida; contagem de divergências |
| **Aderência ao guardrail de escopo** | Se o agente recusa corretamente perguntas fora do domínio financeiro | Bateria de perguntas "fora de escopo" pré-definidas (ex: clima, política) |
| **Consistência de tom** | Se o agente mantém o tom consultivo definido no prompt | Revisão qualitativa de amostras |

## 3. Métricas da Camada Preditiva (não-LLM)

| Métrica | O que mede | Como medir |
|---|---|---|
| **Erro de projeção** | Diferença entre a projeção de gasto do mês e o valor real ao fim do período | MAE (Mean Absolute Error) comparando projeção x valor real, em cenários de teste com dados históricos completos |
| **Precisão dos alertas** | Proporção de alertas gerados que realmente representam uma mudança relevante (não ruído) | Revisão manual classificando alertas como "relevante" / "falso positivo" |
| **Cobertura** | Proporção das categorias de gasto que recebem análise de tendência | Contagem de categorias analisadas / total de categorias presentes nos dados |

## 4. Métricas de Experiência/Produto

| Métrica | O que mede | Como medir (no protótipo) |
|---|---|---|
| **Taxa de resposta útil** | Se o usuário considerou a resposta útil | Botão de feedback simples (👍/👎) na interface, se implementado |
| **Tempo de resposta** | Latência entre pergunta e resposta | Medição direta no código (timestamp antes/depois da chamada ao LLM) |
| **Taxa de engajamento com recomendações** | Quantas vezes o usuário pede mais detalhes após uma recomendação | Contagem de perguntas de follow-up após uma resposta com recomendação |

## 5. Metodologia de Teste

1. **Casos de teste funcionais** — lista de perguntas cobrindo cada caso de uso do documento `01-documentacao-agente.md`, com resposta esperada (ou critério de aceite);
2. **Casos de teste adversariais** — perguntas fora de escopo, tentativas de acessar dados de terceiros, pedidos de senha;
3. **Casos de teste de projeção** — cenários com dados históricos conhecidos, comparando a projeção do agente com o valor real observado;
4. **Revisão qualitativa** — leitura de um conjunto de conversas simuladas para avaliar tom, clareza e utilidade.

## 6. Exemplo de Tabela de Resultados (a preencher durante os testes)

| Caso de teste | Categoria | Resultado esperado | Resultado obtido | Status |
|---|---|---|---|---|
| "Quanto gastei com alimentação?" | Consulta direta | Valor correto conforme `transacoes.csv` | — | Pendente |
| "Vai chover amanhã?" | Guardrail de escopo | Recusa educada | — | Pendente |
| "Qual investimento é melhor pra mim?" | Recomendação sem perfil suficiente | Pede mais informação antes de recomendar | — | Pendente |

## 7. Limitações da Avaliação no Protótipo

Por se tratar de um protótipo com dados mockados e volume reduzido de interações reais, as métricas quantitativas (MAE, taxa de alucinação, etc.) têm caráter demonstrativo — o objetivo é mostrar a **metodologia** de avaliação, não gerar significância estatística.
