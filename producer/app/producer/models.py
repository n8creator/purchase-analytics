from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Item(models.Model):
    """Item model for validation only (without storing data in separate table)."""

    def __init__(self, product_id, quantity, price, category):
        self.product_id = product_id
        self.quantity = quantity
        self.price = Decimal(str(price))
        self.category = category

    def validate(self):
        """Validate item fields."""
        if not isinstance(self.product_id, str):
            raise ValidationError(f"Invalid product_id: {self.product_id}")
        if not isinstance(self.quantity, int) or self.quantity <= 0:
            raise ValidationError(f"Invalid quantity: {self.quantity}")
        if not isinstance(self.price, Decimal) or self.price <= 0:
            raise ValidationError(f"Invalid price: {self.price}")
        if not isinstance(self.category, str):
            raise ValidationError(f"Invalid category: {self.category}")

    def __str__(self):
        return f"{self.product_id} - {self.quantity}x{self.price}, {self.category}"


class Receipt(models.Model):
    """Receipt model for storing customer transactions in database."""

    transaction_id = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField()
    items = models.JSONField(default=list)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    nds_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tips_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50)

    class Meta:
        db_table = "receipts"
        indexes = [
            models.Index(fields=["transaction_id"]),
        ]

    def clean(self):
        """Validate the 'items" JSON field structure and perform additional checks."""
        self._validate_timestamp()
        self._validate_items()
        self._validate_amounts()

    def _validate_timestamp(self):
        """Validate the 'timestamp' field."""
        if self.timestamp > timezone.now():
            raise ValidationError("Timestamp cannot be in the future")

    def _validate_items(self):
        """Validate the 'items' JSON field structure."""
        if not isinstance(self.items, list) or len(self.items) == 0:
            raise ValidationError("Items field must be a non-empty list")

        calculated_total = Decimal("0.00")

        for item_data in self.items:
            item = Item(
                product_id=item_data.get("product_id"),
                quantity=item_data.get("quantity"),
                price=item_data.get("price"),
                category=item_data.get("category"),
            )
            item.validate()  # Validate each item data
            calculated_total += item.price * item.quantity

        if calculated_total != self.total_amount:
            raise ValidationError("Total amount does not match the sum of item prices")

    def _validate_amounts(self):
        """Validate the 'total_amount', 'nds_amount', and 'tips_amount' fields."""
        if self.nds_amount < 0 or self.nds_amount > self.total_amount:
            raise ValidationError("NDS amount must be between 0 and total amount")

        if self.tips_amount is not None and self.tips_amount < 0:
            raise ValidationError("Tips amount cannot be negative")

    def save(self, *args, **kwargs):
        self.full_clean()  # Perform validation before saving the model
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Receipt {self.transaction_id} - {self.timestamp}"
