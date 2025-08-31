from math import e
from django.db import models
from .enums import RuleType, SplitStatus, SplitPaymentMethod
import uuid

class Split(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    effective_date = models.DateTimeField()
    status = models.CharField(choices=SplitStatus.choices, default=SplitStatus.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'split'

class Rules(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    split = models.ForeignKey(Split, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=RuleType.choices, default=RuleType.PERCENTAGE)
    payment_method = models.CharField(choices=SplitPaymentMethod.choices, default=SplitPaymentMethod.PIX)
    recipient_id = models.CharField(max_length=255)
    account_info = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'rule'