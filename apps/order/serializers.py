from rest_framework import serializers
from .models import Order


class OrderRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['user', 'product']