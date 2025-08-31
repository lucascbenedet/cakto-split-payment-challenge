from .PaymentMethodValidatorInterface import PaymentMethodValidatorInterface
from rest_framework.exceptions import ValidationError   

class PixValidator(PaymentMethodValidatorInterface):
    
    def validate(self, account_info: dict):
        if 'pix_key' not in account_info.keys():
            raise ValidationError('Pix key is required')
        return True