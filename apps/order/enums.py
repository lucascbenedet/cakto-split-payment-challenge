from django.db import models

class TransactionStatus(models.TextChoices):
    PENDING = 'pending'
    SUCCESS = 'success'
    FAILED = 'failed'