from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from app.producer.models import Item, Receipt


@pytest.mark.django_db
class TestItemModel:
    def test_item_creation(self):
        item = Item("prod1", 2, "10.50", "category1")
        assert str(item) == "prod1 - 2x10.50, category1"

    @pytest.mark.parametrize(
        "product_id, quantity, price, category, expected_error",
        [
            (123, 2, "10.50", "category1", "Invalid product_id"),
            ("prod1", -1, "10.50", "category1", "Invalid quantity"),
            ("prod1", 2, "-10.50", "category1", "Invalid price"),
            ("prod1", 2, "10.50", 123, "Invalid category"),
        ],
    )
    def test_item_validation(self, product_id, quantity, price, category, expected_error):
        item = Item(product_id, quantity, price, category)
        with pytest.raises(ValidationError, match=expected_error):
            item.validate()


@pytest.mark.django_db
class TestReceiptModel:
    @pytest.fixture
    def valid_receipt_data(self):
        return {
            "transaction_id": "trans1",
            "timestamp": timezone.now(),
            "items": [
                {"product_id": "prod1", "quantity": 2, "price": "10.50", "category": "category1"},
                {"product_id": "prod2", "quantity": 1, "price": "5.00", "category": "category2"},
            ],
            "total_amount": Decimal("26.00"),
            "nds_amount": Decimal("2.60"),
            "payment_method": "card",
        }

    def test_receipt_creation(self, valid_receipt_data):
        receipt = Receipt.objects.create(**valid_receipt_data)
        assert Receipt.objects.count() == 1
        assert str(receipt) == f"Receipt {receipt.transaction_id} - {receipt.timestamp}"

    def test_receipt_validation(self, valid_receipt_data):
        receipt = Receipt(**valid_receipt_data)
        receipt.full_clean()  # Should not raise an exception

    @pytest.mark.parametrize(
        "field, value, expected_error",
        [
            ("timestamp", lambda: timezone.now() + timezone.timedelta(days=1), "Timestamp cannot be in the future"),
            ("items", [], "Items field must be a non-empty list"),
            ("total_amount", Decimal("100.00"), "Total amount does not match the sum of item prices"),
            ("nds_amount", Decimal("-1.00"), "NDS amount must be between 0 and total amount"),
        ],
    )
    def test_receipt_invalid_data(self, valid_receipt_data, field, value, expected_error):
        invalid_data = valid_receipt_data.copy()
        invalid_data[field] = value() if callable(value) else value
        with pytest.raises(ValidationError, match=expected_error):
            Receipt(**invalid_data).full_clean()

    def test_receipt_with_tips(self, valid_receipt_data):
        data_with_tips = valid_receipt_data.copy()
        data_with_tips["tips_amount"] = Decimal("2.00")
        receipt = Receipt.objects.create(**data_with_tips)
        assert receipt.tips_amount == Decimal("2.00")

    def test_receipt_with_negative_tips(self, valid_receipt_data):
        data_with_negative_tips = valid_receipt_data.copy()
        data_with_negative_tips["tips_amount"] = Decimal("-2.00")
        with pytest.raises(ValidationError, match="Tips amount cannot be negative"):
            Receipt(**data_with_negative_tips).full_clean()
