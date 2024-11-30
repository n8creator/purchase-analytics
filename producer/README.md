# 1. First Service (Producer)

## 1.1. Functionality

### 1.1.1. Receiving purchase receipts from clients.

### 1.1.2. Receipt validation: checking for correct format and conformity to the expected structure.

Receipt structure:

```jsonc
{
  "transaction_id": "unique_transaction_id",
  "timestamp": "2024-02-07T12:34:56",
  "items": [
    {
      "product_id": "product_id_1",
      "quantity": 2,
      "price": 10.99,
      "category": "groceries"
    },
    {
      "product_id": "product_id_2",
      "quantity": 1,
      "price": 5.49,
      "category": "electronics"
    }
    // Additional items
  ],
  "total_amount": 27.47,
  "vat_amount": 2.47, // VAT amount
  "tips_amount": 3.0, // Tips amount (if applicable)
  "payment_method": "credit_card"
  // Additional fields as needed
}
```

Mandatory fields:

- `transaction_id`: unique transaction identifier.
- `timestamp`: timestamp of purchase.
- `items`: list of items in the receipt.
- `product_id`: unique product identifier.
- `quantity`: quantity of the product.
- `price`: price of the product.
- `category`: category of the product.
- `total_amount`: total amount of the receipt.
- `vat_amount`: VAT amount.
- `tips_amount`: tips amount (if applicable).
- `payment_method`: payment method.

### 1.1.3. Logging all received receipts.

### 1.1.4. Sending receipts to the second service via Apache Kafka.

## 1.2. Technologies

1. **Django** - for creating an API to receive receipts.
2. **Apache** - Kafka for sending messages to the second service.
3. **Logging** - receipt events for subsequent analysis (in a RDBMS).
4. **RDBMS** - PostgreSQL