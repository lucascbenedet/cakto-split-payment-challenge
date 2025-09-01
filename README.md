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
   git clone https://github.com/lucascbenedet/canto-split-payment-challenge.git
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

5. Crie um super usuário:

   ```bash
   python manage.py createsuperuser
   ```

6. Suba o servidor:

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

   - Admin: `http://localhost:8000/admin/`
   - API: `http://localhost:8000/api/v1/`
   - Documentação: `http://localhost:8000/api/schema/swagger-ui/`

---

### Requisitos de funcionamento

1. Criar um produto:

   - Acesse o endpoint para criar um produto utilizando autorização básica com usuário e senha do superuser criado.

2. Criar regras de splits:
   - É necessário que haja um produto previamente criado para vincular à um split.
   - Sempre que um produto é criado, uma feature flag é criada na tabela config para ele. Para desativar a configuração pra um produto específico é necessário entrar no django admin e desativar a flag.
3. Superuser:

   - O username e password do superuser criado estão no arquivo `.env` para local e `.env.docker` para docker. Por padrão o superuser é criado com o username `cakto` e senha `123`.

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

### Resumo descritivo

- O event sourcing não foi implementado devido ao tempo de entrega e equipe, porém a maneira como o módulo foi criado permite o histórico de todas as configurações. Além disso, facilmente poderia ser integrado um banco de dados NoSQL para escrita dos eventos e a aplicação de um sistema de mensageria que seria responsável por sincronizar os eventos com o banco de dados relacional que já foi estruturado pensando nessa abordagem futura.
- Foi implementado uma tabela de configurações para armazenar as features flags, assim a funcionalidade pode ser disponibilizada para produtos específicos evitando quebra do sistema em produção.
- A tabela `Split` foi criada para armazenar as configurações de cada split, sendo que apenas um split poderia estar ativo por produto. Dessa forma, a validação é feita pelo status do split, o que faz com que todas as regras criadas nunca sejam sobrescritas.
- O módulo de payment representa o fluxo atual do sistema onde o pagamento é processado apenas para o criador do produto. Com o módulo de splits, a configuração do PaymentProcessor foi muito pouco refatorada, apenas tendo que verificar se, para o produto do pedido a configuração de splits está habilitada e se existem regras ativas. Caso existam, o fluxo de pagamento seria feito baseado em cada regra.
- Para representar o fluxo de pagamento foram criadas classes de implementação para processar pagamento em Pix, transfêrencia bancária ou qualquer outro método de pagamento que for necessário. Dessa forma, para cada regra de split o pagamento seria redirecionado para a classe de pagamento específica responsável por àquele método de pagamento.
- Não foi implementado fila de tarefas assíncronas, mas para a entrega do MVP seria necessário que cada regra de pagamento seja processada como uma tarefa assíncrona distinta, para que o sistema não seja bloqueado.
- Foram desenvolvidos testes unitários e de integração em cima da classe `SplitSerivce` para garantir a qualidade do código e a funcionalidade do módulo de splits.
- Também foi desenvolvido métricas e log para a observabilidade que podem ser facilmente incorporadas ao service e posteriormente integradas com algum sistema de monitoramento como Grafana.
- Todas as validações de um split estão dentro do service, concentradas em um só lugar, o que facilita a manutenção e a adição de novas validações caso necessário.

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

### Criar produto

`POST /api/v1/products/`

```json
{
  "name": "Teste",
  "base_value": 100
}
```

### Listar produtos de um usuário

`GET /api/v1/products/`

### Recuperar um produto por id

`GET /api/v1/products/{product_id}/`

---

## 📌 Próximos Passos (evolução real)

- Event sourcing com Kafka para auditoria externa.
- Dashboards Grafana para métricas críticas.

---
