from django.urls import base
import pytest
from decimal import Decimal
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from apps.split_rules.service import SplitSerivce
from apps.split_rules.models import Split, Rules
from django.contrib.auth import get_user_model
from apps.product.models import Product
from apps.split_rules.enums import SplitStatus, SplitPaymentMethod
from rest_framework.test import APIClient
from apps.split_rules.validators import TestValidator
from apps.split_rules.validators.TestValidator import TestValidator
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestSplitService:

    def setup_method(self):
        self.service = SplitSerivce()
        self.user = User.objects.create(username="owner")
        self.other_user = User.objects.create(username="hacker")
        self.product = Product.objects.create(name="Test Product", owner=self.user, base_value=100)

        self.validators = {
            SplitPaymentMethod.PIX: TestValidator(),  
            SplitPaymentMethod.BANK_TRANSFER: TestValidator(),
        }

    def test_should_raise_if_rules_empty(self, rf):
        request = rf.post("/")
        request.user = self.user

        with pytest.raises(ValueError, match="Rules cannot be empty"):
            self.service.create_splits(request, {"product": self.product.id, "rules": []}, self.validators)

    def test_should_raise_if_product_not_found(self, rf):
        request = rf.post("/")
        request.user = self.user

        with pytest.raises(ValueError, match="Product not found"):
            self.service.create_splits(request, {"product": "4ccf9228-acc6-4380-81e3-64182c3d870a", "rules": [{"recipient_id": "x", "type": "percentage", "value": 100, "payment_method": "pix", "account_info": {"pix_key": "a@b.com"}}]}, self.validators)

    def test_should_raise_if_not_owner(self, rf):
        request = rf.post("/")
        request.user = self.other_user

        with pytest.raises(IntegrityError, match="not the owner"):
            self.service.create_splits(request, {"product": self.product.id, "rules": [{"recipient_id": "x", "type": "percentage", "value": 100, "payment_method": "pix", "account_info": {"pix_key": "a@b.com"}}]}, self.validators)

    def test_should_raise_if_active_split_exists(self, rf):
        request = rf.post("/")
        request.user = self.user

        Split.objects.create(product=self.product, status=SplitStatus.ACTIVE, effective_date="2025-01-01T00:00:00Z")

        with pytest.raises(ValueError, match="already exists"):
            self.service.create_splits(request, {"product": self.product.id, "rules": [{"recipient_id": "x", "type": "percentage", "value": 100, "payment_method": "pix", "account_info": {"pix_key": "a@b.com"}}]}, self.validators)

    def test_should_raise_if_percentage_not_100(self, rf):
        request = rf.post("/")
        request.user = self.user

        with pytest.raises(ValidationError, match="must equal 100"):
            self.service.create_splits(request, {"product": self.product.id, "rules": [
                {"recipient_id": "a", "type": "percentage", "value": 70, "payment_method": "pix", "account_info": {"pix_key": "a@b.com"}},
                {"recipient_id": "b", "type": "percentage", "value": 20, "payment_method": "pix", "account_info": {"pix_key": "b@b.com"}},
            ], "effective_date": "2025-01-01T00:00:00Z"}, self.validators)

    def test_should_create_split_and_rules_successfully(self, rf):
        request = rf.post("/")
        request.user = self.user

        data = {
            "product": self.product.id,
            "effective_date": "2025-01-01T00:00:00Z",
            "rules": [
                {"recipient_id": "a", "type": "percentage", "value": 70, "payment_method": "pix", "account_info": {"pix_key": "a@b.com"}},
                {"recipient_id": "b", "type": "percentage", "value": 30, "payment_method": "bank_transfer", "account_info": {"bank": "001", "account": "123"}},
            ]
        }

        self.service.create_splits(request, data, self.validators)

        assert Split.objects.count() == 1
        assert Rules.objects.count() == 2

@pytest.mark.django_db
class TestSplitAPI:

    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="owner", password="pass")
        self.product = Product.objects.create(name="Test Product", owner=self.user, base_value=100)

    def test_create_split_success(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "product": self.product.id,
            "effective_date": "2025-01-01T00:00:00Z",
            "rules": [
                {
                    "recipient_id": "a",
                    "type": "percentage",
                    "value": 70,
                    "payment_method": "pix",
                    "account_info": {"pix_key": "a@b.com"},
                },
                {
                    "recipient_id": "b",
                    "type": "percentage",
                    "value": 30,
                    "payment_method": "bank_transfer",
                    "account_info": {"bank": "001", "account": "123"},
                },
            ],
        }

        res = self.client.post("/api/v1/splits/", payload, format="json")

        assert res.status_code == status.HTTP_201_CREATED
        assert Split.objects.count() == 1
        assert Rules.objects.count() == 2

    def test_create_split_unauthorized(self):
        payload = {"product": self.product.id, "rules": []}
        res = self.client.post("/api/v1/splits/", payload, format="json")

        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_split_not_owner(self):
        other_user = User.objects.create_user(username="hacker", password="pass")
        self.client.force_authenticate(user=other_user)

        payload = {
            "product": self.product.id,
            "effective_date": "2025-01-01T00:00:00Z",
            "rules": [
                {
                    "recipient_id": "a",
                    "type": "percentage",
                    "value": 100,
                    "payment_method": "pix",
                    "account_info": {"pix_key": "a@b.com"},
                }
            ],
        }

        res = self.client.post("/api/v1/splits/", payload, format="json")

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "not the owner" in str(res.data).lower()

    def test_create_split_percentage_not_100(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "product": self.product.id,
            "effective_date": "2025-01-01T00:00:00Z",
            "rules": [
                {"recipient_id": "a", "type": "percentage", "value": 60, "payment_method": "pix", "account_info": {"pix_key": "a@b.com"}},
                {"recipient_id": "b", "type": "percentage", "value": 20, "payment_method": "pix", "account_info": {"pix_key": "b@b.com"}},
            ],
        }

        res = self.client.post("/api/v1/splits/", payload, format="json")

        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "must equal 100" in str(res.data)
