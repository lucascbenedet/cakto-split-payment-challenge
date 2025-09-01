from .PaymentInterface import PaymentInterface
from config.models import Config
from apps.orders.models import Order
from apps.split_rules.models import Split, Rules
from apps.split_rules.enums import SplitStatus
from apps.products.models import Product

class PaymentProcessor:
    def __init__(self, processor: PaymentInterface):
        self.processor = processor
        
    def _verify_payment_split(self, product: Product):
        feature_flag = Config.objects.filter(name="payment_splits", is_active=True, product=order.product)
        rules = Rules.objects.filter(split__product=order.product, split__status=SplitStatus.ACTIVE)
        
        if feature_flag.exists() and rules.exists():
            return rules
        return False
        
    
    def process_payment(self, order: Order):
        # 1. Validate payment method
        # 2. Charge via gateway (Mercado Pago/Pagarme)
        # 3. Update order status
        # 4. Send confirmation
        # 5. Trigger payout to creator (D+2)
        
        rules = self._verify_payment_split(order.product)
        if not rules.exists():
            pass
            #Continua no fluxo de pagamento normal (pagamento sem split) por que não há nenhum split ativo
        
        # Utiliza o fluxo de pagamento em splits para cada uma das regras

        
        