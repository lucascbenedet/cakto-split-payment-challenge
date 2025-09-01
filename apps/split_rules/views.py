from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from .serializers import SplitRequestSerializer, RulesResponseSerializer, UpdateSplitStatusSerializer, SplitResponseSerializer
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
        super().__init__()
        self.service = SplitSerivce()
        
        
    
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
        
        
class UpdateSplitStatus(UpdateAPIView):
    serializer_class = UpdateSplitStatusSerializer
    http_method_names = ["patch"] 

    def __init__(self) -> None:
        super().__init__()
        self.service = SplitSerivce()
        
        
    @extend_schema(request=UpdateSplitStatusSerializer, responses={200: SplitResponseSerializer})
    def partial_update(self, request, split_id , *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            split: Split = self.service.update_split_status(split_id, request.user, serializer.validated_data['status'])
            response_data = SplitResponseSerializer(split).data
            return Response(response_data, status=status.HTTP_200_OK)        
        except exceptions.ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)