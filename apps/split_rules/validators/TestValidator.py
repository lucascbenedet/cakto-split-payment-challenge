from .PaymentMethodValidatorInterface import PaymentMethodValidatorInterface

class TestValidator(PaymentMethodValidatorInterface):
        
    def validate(self, account_info: dict):
        return True
        