from django.db import models
import uuid

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    base_value = models.DecimalField(max_digits=10, decimal_places=2)
    

    class Meta:
        db_table = 'product'