from .PaymentMethodValidatorInterface import PaymentMethodValidatorInterface

class PaymentMethodValidator:
    
    def __init__(self, validator: PaymentMethodValidatorInterface):
        self.validator = validator
        
    def validate(self, account_info: dict):
        self.validator.validate(account_info)
        
    