from rest_framework import serializers
from .models import Product


class ProductRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'base_value']
        
class ProductResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"