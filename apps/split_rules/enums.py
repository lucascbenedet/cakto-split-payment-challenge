from django.db import models

class RuleType(models.TextChoices):
    PERCENTAGE = 'percentage'
    
class SplitStatus(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    ARCHIVED = 'archived'
    

class SplitPaymentMethod(models.TextChoices):
    PIX = 'pix'
    BANK_TRANSFER = 'bank_transfer'