## FRONTEND: Reusable Components

### Introduction

In frontend development, reusable components are essential for ensuring code consistency, efficiency, and maintainability. These components eliminate duplication, reduce errors, and accelerate development cycles by providing modular building blocks that can be integrated across different parts of the project.

The primary focus of this section is to define reusable constants, utility functions, and helper modules that ensure a streamlined development process while adhering to project standards.

---

### Reusable Elements

#### 1. **Constants**
- **Purpose**: Store fixed values used across the application to avoid duplication and ensure consistency.
- **Examples**:
  - **API Endpoints**: Centralize URLs for API requests.
    ```javascript
    export const API_ENDPOINTS = {
      USERS: '/api/users',
      ORDERS: '/api/orders',
      PRODUCTS: '/api/products',
    };
    ```
  - **Common Strings**: Avoid repeated hardcoded strings.
    ```javascript
    export const MESSAGES = {
      SUCCESS: 'Operation completed successfully.',
      ERROR: 'An error occurred. Please try again.',
    };
    ```

#### 2. **Utility Functions**
- **Purpose**: Provide reusable logic for common operations to enhance code maintainability.
- **Examples**:
  - **Data Formatting**: Convert dates, numbers, or strings into specific formats.
    ```javascript
    export const formatDate = (date) => new Intl.DateTimeFormat('en-US').format(date);
    export const formatCurrency = (amount) => `$${amount.toFixed(2)}`;
    ```
  - **Validation Helpers**: Simplify form validations.
    ```javascript
    export const isEmailValid = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    ```

#### 3. **Helper Modules**
- **Purpose**: Encapsulate shared logic into separate modules for cleaner and more readable code.
- **Examples**:
  - **HTTP Requests**:
    ```javascript
    import axios from 'axios';

    export const fetchData = async (url) => {
      try {
        const response = await axios.get(url);
        return response.data;
      } catch (error) {
        throw new Error(error.message);
      }
    };
    ```
  - **LocalStorage Management**:
    ```javascript
    export const saveToLocalStorage = (key, value) => {
      localStorage.setItem(key, JSON.stringify(value));
    };

    export const getFromLocalStorage = (key) => {
      const data = localStorage.getItem(key);
      return data ? JSON.parse(data) : null;
    };
    ```

---

### Standards and Guidelines

1. **Naming Conventions**:
   - Use clear, descriptive names for constants and functions (e.g., `API_ENDPOINTS`, `formatDate`).
   - Follow camelCase for functions and PascalCase for exported objects.

2. **Modularity**:
   - Group related constants and functions in separate files (e.g., `constants.js`, `utils.js`).
   - Avoid monolithic files by splitting functionality into logical modules.

3. **Documentation**:
   - Include comments or JSDoc annotations for complex logic.
   - Provide usage examples where applicable.

4. **Testing**:
   - Write unit tests to verify utility functions and helper modules.
   - Mock external dependencies, such as HTTP requests, during tests.

---

### Implementation

1. **Integration**:
   - Import constants and utilities into components to avoid inline logic or hardcoding.