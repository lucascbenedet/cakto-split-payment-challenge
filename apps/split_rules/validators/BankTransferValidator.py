from .PaymentMethodValidatorInterface import PaymentMethodValidatorInterface
from rest_framework.exceptions import ValidationError

class BankTransferValidator(PaymentMethodValidatorInterface):
    
    def validate(self, account_info: dict):
        if 'bank' not in account_info:
            raise ValidationError('Field bank is required in account_info for bank_transfer method')
        if 'account' not in account_info:
            raise ValidationError("Field account is required in account_info for bank_transfer method")
        
        return True