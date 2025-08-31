from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView
from .serializers import SplitRequestSerializer
from .models import Split, Rules
from .service import SplitSerivce
from rest_framework import exceptions
from rest_framework import status
from rest_framework.response import Response
from .enums import SplitPaymentMethod
from .validators.BankTransferValidator import BankTransferValidator
from .validators.PixValidator import PixValidator
from .service import SplitSerivce
from rest_framework import serializers
from django.db import IntegrityError


class CreateSplits(CreateAPIView):
    serializer_class = SplitRequestSerializer
    validators = {
        SplitPaymentMethod.PIX: PixValidator(),
        SplitPaymentMethod.BANK_TRANSFER: BankTransferValidator(),
    }
    
    def __init__(self) -> None:
        self.service = SplitSerivce()
        super().__init__()
        
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.service.create_splits(request, serializer.validated_data, validators=self.validators)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)
        
        
        
