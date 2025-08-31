# Usa Python 3.13
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#ENV POETRY_VERSION=1.8.3
RUN curl -sSL https://install.python-poetry.org | python3 -

# Adiciona Poetry ao PATH
ENV PATH="/root/.local/bin:$PATH"

# Cria diretório da aplicação
WORKDIR /app

# Copia arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instala dependências sem criar venv (usa o sistema)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copia o código do projeto
COPY . .

# Expõe porta 8000
EXPOSE 8000

# Comando padrão (Gunicorn já configurado no docker-compose)
CMD ["gunicorn", "src.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
