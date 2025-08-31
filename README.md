# Cakto Split Payment Challenge

Implementação de um módulo de **Split Payments** em Django REST Framework, atendendo aos requisitos de escalabilidade, auditoria e observabilidade descritos no desafio.

---

## 📦 Stack Utilizada

- **Django 5 + Django REST Framework** → API REST e modelo de dados.
- **PostgreSQL** → banco relacional com integridade financeira.
- **pytest + pytest-django** → testes unitários e de integração.
- **Prometheus Client** → métricas de observabilidade.
- **Docker + docker-compose** → containerização do ambiente.

---

## 🚀 Como Rodar o Projeto

### Pré-requisitos

- Python 3.13+ (ou superior)
- Docker e Docker Compose

### Rodando localmente (sem Docker)

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu-user/cakto-split-payment-challenge.git
   cd cakto-split-payment-challenge
   ```

2. Crie o ambiente virtual e instale dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install poetry
   poetry install
   ```

3. Configure o arquivo .env com as credenciais do banco de dados.

4. Rode as migrações:

   ```bash
   python manage.py migrate
   ```

5. Suba o servidor:

   ```bash
   python manage.py runserver
   ```

---

### Rodando com Docker

1. Suba os containers:

   ```bash
   docker-compose up --build
   ```

2. Acesse:

   - API: `http://localhost:8000/api/v1/`
   - Documentação: `http://localhost:8000/api/schema/swagger-ui/`

---

## 🧪 Testes

### Unitários e Integração

Os testes cobrem:

- Serviço de criação de splits (`SplitService`).
- API `POST /api/v1/splits/`.
- Validações de negócio (percentuais, owner do produto, split duplicado).
- Fluxos felizes e de erro.

Rodando testes localmente:

```bash
pytest
```

Rodando testes dentro do container:

```bash
docker-compose exec web pytest
```

---

## 📊 Decisões Técnicas

### Arquitetura

- **Monólito modular em Django**: escolhido pelo prazo de MVP (6 semanas) e compatibilidade com stack existente. Evita overhead de microsserviço, mas mantém separação em módulo (`split_rules`).
- **Consistência**: transações atômicas garantem que split e regras sejam criados juntos ou revertidos em caso de erro.
- **Event sourcing**: não implementado no MVP, mas a tabela `Rules` atua como histórico auditável.
- **Deploy**: pensado para ser canário (sem downtime) em Docker/K8s.
- **Escalabilidade**: PostgreSQL com índices (`product_id`, `split_id`) e possibilidade de particionamento em `rules`.

### Banco de Dados

- **Tabela `Split`** → configuração ativa por produto.
- **Tabela `Rules`** → histórico detalhado de todas as regras.
- **Constraints**:

  - Apenas 1 split ativo por produto.
  - Soma de regras deve dar 100%.
  - `CHECK` em valores inválidos.

- **Auditoria embutida**: `created_at`, `updated_at`.

---

## 📊 Observabilidade

### Logs

- Configurados no `settings.py`, enviados para **stdout** (coletado em Docker/K8s).
- O módulo se adaptaria ao padrão de logs definidos no projeto principal.
- Bastaria configurar o caminho para um sistema de log externo como DataDog se necessário.
- Exemplo:

  ```json
  {
    "time": "2025-08-31T14:00:00",
    "level": "INFO",
    "logger": "split-payments",
    "message": "Split created"
  }
  ```

### Métricas Prometheus

Expostas em `/metrics` via `prometheus_client`.

- **Counters**:

  - `splits_created_total{product_id}` → total de splits criados.
  - `splits_failed_total{reason}` → falhas de criação.
  - `split_anomalies_total{type}` → inconsistências detectadas.

- **Histogram**:

  - `split_latency_seconds` → latência do `SplitService`.

### Thresholds sugeridos

- `rate(splits_failed_total[5m]) > 5` → alerta de falha.
- `histogram_quantile(0.95, split_latency_seconds) > 0.5` → latência p95 acima de 500ms.
- `split_anomalies_total > 0` → incidente crítico.

---

## 📊 Endpoints Principais

### Criar split

`POST /api/v1/splits/`

```json
{
  "product": "uuid-produto",
  "effective_date": "2025-01-01T00:00:00Z",
  "rules": [
    {
      "recipient_id": "user_creator",
      "type": "percentage",
      "value": 65,
      "payment_method": "bank",
      "account_info": { "bank": "001", "account": "12345-6" }
    },
    {
      "recipient_id": "user_partner",
      "type": "percentage",
      "value": 35,
      "payment_method": "pix",
      "account_info": { "pix_key": "partner@email.com" }
    }
  ]
}
```

### Respostas

- `201 Created` → split criado.
- `400 Bad Request` → validação falhou (ex: soma ≠ 100%).
- `401 Unauthorized` → usuário não autenticado.
- `403 Forbidden` → usuário não é dono do produto.

---

## 📌 Próximos Passos (evolução real)

- Event sourcing com Kafka para auditoria externa.
- Feature flags centralizadas (ex: LaunchDarkly).
- Deploy blue/green com rollback automático.
- Dashboards Grafana para métricas críticas.

---
