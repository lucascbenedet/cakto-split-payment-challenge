# Split Payments - Documentação Técnica

## Validações de Negócio Necessárias

### Validações de Configuração de Split

- **Soma de percentuais**: A soma de todos os percentuais deve ser exatamente 100%

- **Valores mínimos**: Cada split deve ter valor mínimo de R$ 0,01 para evitar problemas de arredondamento

- **Regras únicas**: Cada produto só pode ter uma configuração de regras de split.

- **Validação de contas**: Verificar se as contas bancárias/PIX dos recipients são válidas

- **Data de vigência**: `effective_date` não pode ser retroativa

- **Recipient ativo**: Não foi especificado no documento, mas caso necessário verificar se o recipient possui conta na plataforma.

### Validações de Processamento

- **Valor mínimo da transação**: Transação deve ter valor mínimo que permita splits sem perda de centavos

- **Status do produto**: Produto deve estar ativo e possuir a flag ativa para a nova feature de splits

### Validações de Integridade Financeira

- **Precisão decimal**: Garantir que não haja perda de centavos nos cálculos

- **Reconciliação**: Valor total dos splits deve ser igual ao valor da transação original

- **Auditoria**: Manter rastro completo de todas as operações para compliance

## Estados Possíveis de um Split

### Estados de Configuração

- **ACTIVE**: Split ativo e processando transações

- **INACTIVE**: Split criado, mas desabilitado

- **CANCELLED**: Split cancelado permanentemente, ou excluído por soft delete

## Como Lidar com Alterações de Configuração

### Estratégia de Versionamento de Configurações

- **Imutabilidade**: Configurações existentes nunca são alteradas, apenas desativadas, ou excluídas para criação de uma nova.

- **Versionamento temporal**: Nova configuração com `effective_date` futura, por exemplo a maior effective_date é a que vale, assim mantém a auditoria das configurações.

### Estratégias de Versionamento

1. **URL Path Versioning**

```
POST /api/v1/splits/
POST /api/v2/splits/
```

- Em caso de alteração de funcionalidade, incluí-la na rota com a nova versão, mantendo ambas as versões da API disponíveis para compatibilidade com diferentes clientes.
