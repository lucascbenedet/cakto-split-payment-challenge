from ast import List
from bdb import effective
from decimal import Decimal, ROUND_HALF_UP
from operator import is_
from apps import product
from django.db import transaction as db_transaction
from .models import Split, Rules
from .enums import SplitPaymentMethod, RuleType, SplitStatus
from django.contrib.auth.models import Permission, User
from .validators.PaymentMethodValidator import PaymentMethodValidator
from .validators.PaymentMethodValidatorInterface import PaymentMethodValidatorInterface
from rest_framework.exceptions import ValidationError
from ..product.models import Product
from rest_framework.exceptions import PermissionDenied
from . import monitoring



class SplitSerivce:
    
    @monitoring.measure_latency
    @db_transaction.atomic
    def create_splits(self,request, validated_data, validators: dict[str, PaymentMethodValidatorInterface]): 
            
        rules = validated_data['rules']
        if not rules:
            raise ValueError("Rules cannot be empty")
        try:
            product = Product.objects.get(id=validated_data['product'])
            if request.user != product.owner:
                raise PermissionDenied("You are not the owner of this product")       
        except Product.DoesNotExist:
            raise ValueError("Product not found")
        
        
        if Split.objects.filter(product=product, status=SplitStatus.ACTIVE).exists():
            raise ValueError("Active split for the product already exists")
       
        split = Split.objects.create(product=product, effective_date=validated_data['effective_date'])    
        
        rules_objects: List[Rules] = []
        percent_value = Decimal('0')
        for rule in rules:
            try:
                percent_value += Decimal(str(rule['value']))
            except (ValueError, TypeError, ArithmeticError):
                raise ValidationError("Invalid percentage value in rules.")
            
            method = rule.get('payment_method')
            method_validator = validators.get(method)
            payment_validator = PaymentMethodValidator(method_validator)
            payment_validator.validate(rule['account_info'])
            
            
            rules_objects.append(
                Rules(
                    split = split,
                    **rule
                )
            )
        if percent_value != Decimal('100'):
            raise ValidationError(f"The total percentage of split rules must equal 100.")
        
        Rules.objects.bulk_create(rules_objects)
            
                
                