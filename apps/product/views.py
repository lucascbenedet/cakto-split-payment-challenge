from django.http import request
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductResponseSerializer, ProductRequestSerializer
from .service import ProductService
from drf_spectacular.utils import extend_schema


class ListCreateProductView(ListCreateAPIView):
    serializer_class = ProductResponseSerializer
    request_serializer = ProductRequestSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()
    
    def get_queryset(self):
        return self.service.get_all_products(self.request.user)
    
    @extend_schema(request=request_serializer, responses={201: ProductResponseSerializer})
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.request_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            product = self.service.create_product(request, serializer.validated_data)
            response_data = self.get_serializer(product).data
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class RetrieveProductView(RetrieveAPIView):
    serializer_class = ProductResponseSerializer
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()
    
    
    def retrieve(self, request, pk, *args, **kwargs):
        product = self.service.get_product_by_id(pk)
        response_data = self.serializer_class(product).data
        return Response(response_data, status=status.HTTP_200_OK)
    
        
        

    