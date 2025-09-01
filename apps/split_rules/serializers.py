from bdb import effective
from itertools import product
from .models import Split, Rules
from .enums import SplitStatus
from rest_framework import serializers, status



class RulesRequestSerializer(serializers.ModelSerializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Rules
        fields = ['value', 'type', 'payment_method', 'account_info', 'recipient_id']
        
class RulesResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = ['id', 'value', 'type', 'payment_method', 'account_info', 'recipient_id', 'split']
        
class SplitRequestSerializer(serializers.Serializer):
    product = serializers.UUIDField(required=True)
    rules = RulesRequestSerializer(many=True, required=True)
    effective_date = serializers.DateTimeField(required=True)
    
class UpdateSplitStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=SplitStatus.choices, required=True)
    
class SplitResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Split
        fields = ['id', 'product', 'effective_date', 'status']