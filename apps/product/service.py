from .models import Product


class ProductService:
    
    def get_product_by_id(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValueError("Product not found.")
        
    def get_all_products(self, user):
        return Product.objects.filter(owner=user)
    
    def create_product(self,request, validated_data):
        return Product.objects.create(owner=request.user, **validated_data)