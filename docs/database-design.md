# Database Design

## Objetivos

- Garantir integridade financeira (sem perda de centavos).
- Manter histórico e auditoria de todas as regras aplicadas.
- Suportar consultas de alta frequência para validação e reconciliação.
- Permitir evolução futura sem quebra de compatibilidade.

## Entidades Principais

### `splits`

Tabela responsável por armazenar a configuração ativa de split para um produto.

| Coluna         | Tipo      | Descrição                                          |
| -------------- | --------- | -------------------------------------------------- |
| id             | UUID (PK) | Identificador único do split                       |
| product_id     | VARCHAR   | Identificador do produto (único ativo por produto) |
| status         | ENUM      | Estados:  `active`, `inactive`, `archived` |
| effective_date | TIMESTAMP | Data de entrada em vigor                           |
| created_at     | TIMESTAMP | Auditoria de criação                               |
| updated_at     | TIMESTAMP | Auditoria de atualização                           |

**Constraints:**

- `UNIQUE (product_id, status='active')` → garante apenas um split ativo por produto.
- `CHECK (effective_date >= now())` → impede ativação retroativa inválida.

---

### `rules`

Histórico de regras de distribuição associadas a um split.

| Coluna       | Tipo          | Descrição                    |
| ------------ | ------------- | ---------------------------- |
| id           | UUID (PK)     | Identificador único da regra |
| split_id     | UUID (FK)     | Referência para `splits(id)` |
| recipient_id | VARCHAR       | Identificador do recebedor   |
| type         | ENUM          | `percentage`                 |
| value        | DECIMAL(10,2) | Percentual                   |
| account_info | JSONB         | Dados bancários / PIX        |
| created_at   | TIMESTAMP     | Auditoria de criação         |

**Constraints:**

- `CHECK (type='percentage' e somatório de value == 100)` → evita configuração inválida.

- `FOREIGN KEY (split_id)` → Mantém a integridade das regras e splits.

---

## Estratégias de Escala e Performance

- **Índices para performances em consultas frequêntes:**
  - `idx_splits_product_id`
  - `idx_rules_split_id`
- **Particionamento:**
  - Tabela `rules` pode ser particionada por `split_id` ou por período (`created_at`) para suportar 10k+ transações/hora.
- **Auditoria:**
  - `rules` nunca é sobrescrita, sempre criada nova versão, assim garante o histórico completo de regras criadas pra um produto.
  - `splits` armazena todos os splits já criados, assim o usuário consegue consultar e ativar novamente splits criados anteriormente.

---
