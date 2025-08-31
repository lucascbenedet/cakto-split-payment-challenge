from django.db import models

class Config(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'sys_config'
