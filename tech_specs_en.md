# Tech Specs for Implementing Services using Apache Kafka, Django, Celery

## About

The purpose of this project is to create two services, connected via Apache Kafka, for processing and analyzing purchase receipts. The first service is responsible for receiving, validating, and logging receipts, as well as forwarding them to the second service. The second service parses the contents of receipts, associates them with purchase locations, performs analytics, and provides data via an API.

## 1. First Service (Producer)

### 1.1. Functionality

#### 1.1.1. Receiving purchase receipts from clients.

#### 1.1.2. Receipt validation: checking for correct format and conformity to the expected structure.

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

#### 1.1.3. Logging all received receipts.

#### 1.1.4. Sending receipts to the second service via Apache Kafka.

### 1.2. Technologies

1. **Django** - for creating an API to receive receipts.
2. **Apache** - Kafka for sending messages to the second service.
3. **Logging** - receipt events for subsequent analysis (in a RDBMS).
4. **RDBMS** - PostgreSQL

## 2. Second Service (Consumer)

### 2.1. Functionality

#### 2.1.1. Receiving receipts from the first service via Apache Kafka.

#### 2.1.2. Parsing the contents of receipts to associate them with purchase locations and additional information (e.g., purchase categories).

Analytics structure:

```json
{
  "place_id": "unique_place_id",
  "place_name": "Store ABC",
  "total_purchases": 150,
  "average_receipt": 35.75,
  "taxes_amount": {
    "total_vat": 275.0,
    "total_tips": 150.0
  },
  "category_analytics": {
    "groceries": {
      "total_spent": 5000.0,
      "average_receipt": 25.0
    },
    "electronics": {
      "total_spent": 3000.0,
      "average_receipt": 50.0
    }
    // Other categories
  }
  // Other metrics
}
```

Mandatory fields:

- `place_id`: unique identifier of the purchase location.
- `place_name`: name of the purchase location.
- `total_purchases`: total number of purchases at this location.
- `average_receipt`: average receipt at this location.
- `taxes_amount`: total amount of taxes and tips.
- `total_vat`: total VAT amount for the time period.
- `total_tips`: total tips amount for the time period.
- `category_analytics`: analytics by product categories.
- `total_spent`: total amount spent on the category for the time period.
- `average_receipt`: average receipt for the category.

#### 2.1.3. Saving data to the database.

#### 2.1.4. Calculation of analytics:

- Number of purchases at each location.
- Average receipt at each location.
- Total amount of taxes and tips for the time period.
- Analytics by product categories.

#### 2.1.5. Scheduling analytics calculations every hour using Celery.

## 2.2. Technologies

1. **Django** - for creating an API for processing receipts and providing data.
2. **Apache Kafka** - for receiving messages from the first service.
3. **RDBMS** - PostgreSQL.
4. **Celery** - for periodically scheduling tasks for analytics calculation.

## 3. API Requirements

### 3.1. Endpoints

### 3.1.1 First Service:

- `POST /api/checks/` - receipt submission.

### 3.1.2 Second Service:

- `GET /api/places/` - retrieve list of purchase locations.
- `GET /api/analytics/` - retrieve overall analytics.
- Additional endpoints as needed.

### 3.2. Authentication

- Token-based authentication and authorization.
- Access control to different parts of the API based on roles.

## 4. Documentation

- Creation of API documentation using Swagger or another tool.
- Deployment and configuration documentation for the services.

## 5. Containerization

Mandatory condition for completing the test assignment is to assemble the final solution using Docker.

## 6. Conclusion

The project's goal is to ensure efficient exchange and processing of purchase receipt data between two services. The services should be scalable, reliable, and provide convenient access to analytical data through the API.
