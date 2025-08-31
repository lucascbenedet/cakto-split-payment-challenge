import logging
import time
from prometheus_client import Counter, Histogram

logger = logging.getLogger("split-payments")

# Contador de splits criados
splits_created_total = Counter(
    "splits_created_total",
    "Número total de splits criados",
    ["product_id"]
)

# Contador de falhas na criação de splits
splits_failed_total = Counter(
    "splits_failed_total",
    "Número total de falhas ao criar splits",
    ["reason"]
)

# Latência de processamento de splits
split_latency_seconds = Histogram(
    "split_latency_seconds",
    "Latência para criar/processar splits em segundos",
    buckets=(0.1, 0.3, 0.5, 1, 2, 5)
)

# Anomalias detectadas (ex: soma != 100)
split_anomalies_total = Counter(
    "split_anomalies_total",
    "Número de splits inválidos detectados",
    ["type"]
)


def log_split_created(product_id: str):
    """Loga e incrementa métrica de split criado"""
    logger.info("Split created", extra={"product_id": product_id})
    splits_created_total.labels(product_id=product_id).inc()


def log_split_failed(reason: str, product_id: str = None):
    """Loga falha e incrementa métrica de erro"""
    logger.warning("Split creation failed", extra={"product_id": product_id, "reason": reason})
    splits_failed_total.labels(reason=reason).inc()


def log_split_anomaly(anomaly_type: str, details: dict = None):
    """Loga inconsistência/anomalia de regra"""
    logger.error("Split anomaly detected", extra={"type": anomaly_type, "details": details})
    split_anomalies_total.labels(type=anomaly_type).inc()


def measure_latency(func):
    """Decorator para medir tempo de execução"""
    def wrapper(*args, **kwargs):
        start = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            duration = time.time() - start
            split_latency_seconds.observe(duration)
            logger.debug(f"Latency measured: {duration:.4f}s", extra={"func": func.__name__})
    return wrapper
