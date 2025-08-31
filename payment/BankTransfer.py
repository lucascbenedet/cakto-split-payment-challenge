from .PaymentInterface import PaymentInterface

class BankTransfer(PaymentInterface):
    
    def process_payment(self, value, account_info):
        pass