# Execution Plan

## Sprint 1-2: Foundation

**Prioridades:**

- Definir modelo de dados (`splits` e `rules`).
- Implementar migrações e constraints financeiras.
- Criar endpoints básicos da API (`POST /splits/`, `GET /splits/:id`).
- Setup de observabilidade inicial (logs estruturados, métricas básicas).

**Componentes paralelizáveis:**

- Banco de dados + migrations.
- API endpoints.

---

## Sprint 3-4: Core Implementation

**Marcos técnicos:**

- Implementar serviço de cálculo de split (precisão com `Decimal`).
- Garantir atomicidade → uso de transações para `splits` + `rules`.
- Implementar validações de negócio:
  - Somatório de `rules.value` = 100% (se percentual).
  - Apenas um split ativo por produto.
- Implementar auditoria (versões de regras no histórico).
- Integração com o processamento de pagamento atual.
- Estratégia de versionamento da API (`/api/v1/splits`).

**Testes:**

- Unitários: serviços de cálculo e validações.
- Integração: fluxo completo de criação → processamento → payout.
- Carga: simulação de 10k transações/hora.

**Garantia de qualidade:**

- Revisões de PR obrigatórias.
- Linter + testes rodando no CI/CD.
- Feature flag para rollout gradual.

---

## Sprint 5-6: Production Readiness

**Critérios de go-live:**

- Latência < 200ms para criação de splits.
- Testes de carga estáveis (10k transações/hora sem erro).
- Documentação atualizada (API + banco de dados).

**Plano de rollback:**

- Versões de banco versionadas via migrações.
- Deploy canário com rollback automático se falhar.
- Configuração de feature flag para desativação da funcionalidade facilmente.

**Monitoramento e alertas:**

- Métricas críticas:
  - Latência por endpoint.
  - Falhas em transações de split.
  - Desbalanceamento de regras (>100% ou <100%) e cálculo do valor no momento de processar o pagamento.
- Alertas automáticos em DataDog / New Relic.
