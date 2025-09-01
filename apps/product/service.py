from .models import Product
from config.models import Config


class ProductService:
    
    def get_product_by_id(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError("Product not found.")
        
    def get_all_products(self, user):
        return Product.objects.filter(owner=user)
    
    def create_product(self,request, validated_data):
        product = Product.objects.create(owner=request.user, **validated_data)
        Config.objects.create(name="payment_splits", is_active=True, product=product)
        return product