# Architecture Decisions

## Decisão 1 – Módulo monolítico evolutivo (híbrido)

- Opção escolhida: implementar Split Payments como um app Django dentro do monólito atual.
- Por quê:
  - Integração e entrega mais rápidas devido ao reuso de auth, deploy, observabilidade e conexão com o banco de dados.
  - Menor risco e overhead operacional no MVP. Como a equipe é pequena, não faz sentido adicionar a complexidade de um microserviço que precisaria de uma arquietetura, lógica e deploy exlusivo.
  - Prepara migração futura para microserviço (caso haja necessidade de escalar apenas esse módulo).

## Decisão 2 – Consistência, atomicidade

- Técnicas:
  - `transaction.atomic` para criar cada split no mesmo commit.
  - Unique constraints para idempotência como por exemplo uma idenpotency_key única por transação para evitar que os splits sejam aplicados mais de uma vez.
- Por quê:
  - Evitar duplicidade de splits.
  - Garantir que ou tudo é persistido, ou nada (integridade financeira).

## Decisão 3 – Event sourcing vale a pena?

- Sim, event sourcing é uma ótima solução de auditoria dependendo do domínio. Para o mercado financeiro é muito interessante que todos os eventos (ações) realizados pelo usuário sejam registradas e que o estado atual do banco de dados seja uma consequência do fluxo de eventos.
- Porém, devido ao tempo e a estrutura da equipe é muito pouco provável que incluir event sourcing no MVP seja uma solução adequada, pois adiciona uma complexidade bem maior.
- Inicialmente pode se trabalhar com uma arquietura normal, com banco relacional e endpoints que lidem com ações múltiplas, como processar uma transação e criar os splits refrêntes a ela.
- No entando, futuramente, após a funcionalidade madura e devidamente implementada pode se considerar a inclusão de um banco de dados de escrita que registre os eventos e algum sistema de mensageria que processe cada evento e os estruture em um banco de dados relacional de leitura.

## Decisão 4 – Deploy sem downtime

- Estratégia:
  - Uma ótima maneira de realizar um deploy sem downtime é utilizar uma flag para a feature. Por exemplo, o banco de dados armazenaria a configuração de ativação ou não da feature para cada produto. Com isso poderia ser definido qual produto receberia essa feature e assim, ativando a funcionalidade apenas para testers ou usuários específicos.
  - Além disso, algo que poderia ser feito para testar a funcionalidade seria roda-la em paralelo ao processamento normal do pagamento, mas apenas gerando logs para verficiar se a divisão do pagamento foi realizada como esperado.
- Por quê:
  - Serviço de pagamentos exige alta disponibilidade;
  - A funcionalidade simplemente pode ser desativada apenas com uma flag em caso de erro.
  - Testes seriam realizados apenas com uma parcela muito pequena de usuários antes de ser habilitada para todos.

## Decisão 5 – Métricas e observabilidade críticas

- Precisão no cálculo dos splits.
  - Garantir que o somatório dos splits para aquele pedido corresponda ao valor total do pagamento.
  - Garantir que os splits são distribuídos de forma justa, ou seja, que o valor de cada split seja igual ou maior que zero.

## Decisão 6 – Precisão financeira

- Decimal (numeric) end-to-end, sem float.
- Estratégia de arredondamento: largest remainder para distribuir centavos residuais de modo justo.
- Somatórios e checks de integridade no DB.

## Decisão 7 – Escalabilidade e concorrência

- Postgres: índices adequados, partição por tempo em tabelas de operações (payment_split/item).
- Redis: cache tático e controle de deduplicação/locks (com parcimônia).
- Processamento assíncrono: Celery, filas por prioridade, prefetch baixo, `acks_late`, DLQ.

## Decisão 8 – Segurança e compliance

- Segregação de dados sensíveis; tokenização quando aplicável.
- HMAC para webhooks; proteção a replay; audit log imutável.
- Princípio do menor privilégio em credenciais e rotinas de rotação.

## Trade-offs chave

- Time-to-market vs pureza arquitetural: priorizamos módulo monolítico com bons boundaries.
- Exactly-once vs at-least-once: adotamos at-least-once com idempotência, padrão de mercado em pagamentos.
- Event sourcing: adiado; MVP com outbox e auditoria cobre necessidades.
