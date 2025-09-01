from rest_framework import serializers
from .models import Product


class ProductRequestSerializer(serializers.Serializer):
    base_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    name = serializers.CharField(max_length=255)
        
class ProductResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"