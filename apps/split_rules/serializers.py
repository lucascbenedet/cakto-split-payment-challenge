from bdb import effective
from itertools import product
from .models import Split, Rules
from rest_framework import serializers



class RulesRequestSerializer(serializers.ModelSerializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Rules
        fields = ['value', 'type', 'payment_method', 'account_info', 'recipient_id']
        
class SplitRequestSerializer(serializers.Serializer):
    product = serializers.UUIDField(required=True)
    rules = RulesRequestSerializer(many=True, required=True)
    effective_date = serializers.DateTimeField(required=True)