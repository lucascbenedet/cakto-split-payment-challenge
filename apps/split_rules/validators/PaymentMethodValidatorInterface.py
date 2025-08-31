from rest_framework.exceptions import ValidationError

class PaymentMethodValidatorInterface:
    
    def validate(self, account_info: dict):
        pass
    
    