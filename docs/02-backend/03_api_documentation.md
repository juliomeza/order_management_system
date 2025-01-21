# API Documentation

## 1. API Overview

### 1.1 Base URL Structure
- Production: `https://api.domain.com/v1`
- Staging: `https://api.staging.domain.com/v1`
- Development: `https://api.dev.domain.com/v1`

### 1.2 Authentication
- Bearer token authentication
- Format: `Authorization: Bearer <token>`
- Token expiration: 24 hours
- Refresh token mechanism available

### 1.3 Standard Response Format

#### Success Response
```json
{
    "status": "success",
    "data": {
        // Response data here
    },
    "metadata": {
        "page": 1,
        "perPage": 20,
        "total": 100
    }
}
```

#### Error Response
```json
{
    "status": "error",
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable message",
        "details": {
            // Additional error details
        }
    }
}
```

## 2. API Endpoints

### 2.1 Authentication Endpoints

#### Login
```
POST /auth/login
```
Request:
```json
{
    "username": "string",
    "password": "string"
}
```
Response:
```json
{
    "status": "success",
    "data": {
        "accessToken": "string",
        "refreshToken": "string",
        "expiresIn": 86400
    }
}
```

#### Refresh Token
```
POST /auth/refresh
```
Request:
```json
{
    "refreshToken": "string"
}
```
Response:
```json
{
    "status": "success",
    "data": {
        "accessToken": "string",
        "expiresIn": 86400
    }
}
```

### 2.2 Order Management Endpoints

#### Create Order
```
POST /orders
```
Request:
```json
{
    "projectId": "string",
    "warehouseId": "string",
    "carrierId": "string",
    "serviceTypeId": "string",
    "expectedDeliveryDate": "date",
    "shippingAddress": {
        // Address details
    },
    "items": [
        {
            "materialId": "string",
            "quantity": "number"
        }
    ]
}
```
Response:
```json
{
    "status": "success",
    "data": {
        "orderId": "string",
        "orderNumber": "string",
        // Additional order details
    }
}
```

#### Get Order Details
```
GET /orders/{orderId}
```
Response:
```json
{
    "status": "success",
    "data": {
        // Complete order details
    }
}
```

#### List Orders
```
GET /orders
```
Query Parameters:
- page (default: 1)
- perPage (default: 20)
- status
- dateFrom
- dateTo
- projectId

### 2.3 Inventory Management Endpoints

#### Get Inventory Levels
```
GET /inventory
```
Query Parameters:
- warehouseId
- materialId
- projectId

#### Update Inventory
```
POST /inventory/adjust
```
Request:
```json
{
    "materialId": "string",
    "quantity": "number",
    "reason": "string",
    "reference": "string"
}
```

### 2.4 Customer Management Endpoints

#### Create Customer
```
POST /customers
```
Request:
```json
{
    "name": "string",
    "code": "string",
    "address": {
        // Address details
    },
    "settings": {
        "outputFormat": "CSV|JSON",
        // Additional settings
    }
}
```

#### Update Customer
```
PUT /customers/{customerId}
```

#### List Customers
```
GET /customers
```

## 3. Security Implementation

### 3.1 Rate Limiting
- Anonymous requests: 60 requests per hour
- Authenticated requests: 1000 requests per hour
- Custom limits available per endpoint

### 3.2 CORS Configuration
```json
{
    "allowedOrigins": [
        "https://app.domain.com",
        "https://admin.domain.com"
    ],
    "allowedMethods": ["GET", "POST", "PUT", "DELETE"],
    "allowCredentials": true,
    "maxAge": 86400
}
```

### 3.3 Data Validation
- Input sanitization on all endpoints
- Type checking and validation
- Size limits on request payloads
- File upload restrictions

## 4. Error Codes and Handling

### 4.1 Standard Error Codes
- 1000: Authentication Error
- 2000: Authorization Error
- 3000: Validation Error
- 4000: Business Logic Error
- 5000: System Error

### 4.2 Error Response Examples

#### Validation Error
```json
{
    "status": "error",
    "error": {
        "code": "3000",
        "message": "Validation failed",
        "details": {
            "quantity": "Must be greater than 0",
            "materialId": "Invalid material ID"
        }
    }
}
```

#### Business Logic Error
```json
{
    "status": "error",
    "error": {
        "code": "4000",
        "message": "Insufficient inventory",
        "details": {
            "available": 10,
            "requested": 15
        }
    }
}
```

## 5. API Versioning

### 5.1 Version Control
- Major versions in URL path (/v1, /v2)
- Minor versions handled through headers
- Deprecation notices provided 6 months in advance

### 5.2 Backwards Compatibility
- Breaking changes only in major versions
- Deprecated fields marked in responses
- Migration guides provided for major updates

## 6. API Monitoring

### 6.1 Metrics Collection
- Request duration
- Error rates
- Endpoint usage
- Response sizes
- Cache hit rates

### 6.2 Health Checks
```
GET /health
```
Response:
```json
{
    "status": "success",
    "data": {
        "status": "healthy",
        "version": "string",
        "timestamp": "string"
    }
}
```