## FRONTEND: API Integration

### Introduction

API integration is a critical aspect of modern frontend development. A robust integration ensures efficient communication between the frontend and backend, secure data handling, and a seamless user experience. This document outlines best practices, tools, and patterns for integrating APIs in the project.

---

### Tools and Libraries

1. **Axios**:
   - Easy-to-use HTTP client for making API requests.
   - Supports request and response interceptors for centralized handling.
   - Provides built-in support for timeout and cancellation.

2. **Fetch**:
   - Native browser API for making HTTP requests.
   - Lightweight and widely supported, but requires more boilerplate code.

For this project, **Axios** is recommended due to its enhanced features and developer-friendly syntax.

---

### API Integration Workflow

#### 1. **Setup and Configuration**

- Create a centralized Axios instance for consistent configuration:
  ```javascript
  import axios from 'axios';

  const apiClient = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL,
    timeout: 10000, // 10 seconds
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Request Interceptor
  apiClient.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response Interceptor
  apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response && error.response.status === 401) {
        // Handle token expiration
      }
      return Promise.reject(error);
    }
  );

  export default apiClient;
  ```

- Store the base URL and other environment-specific variables in `.env` files:
  ```plaintext
  REACT_APP_API_BASE_URL=https://api.example.com
  ```

#### 2. **Authentication Handling**

- Use **JSON Web Tokens (JWT)** for secure authentication:
  - Store tokens securely:
    - Use `HttpOnly cookies` for better security.
    - If using `localStorage`, ensure tokens are cleared on logout.
  - Refresh tokens:
    - Implement a silent token renewal mechanism before expiration.

#### 3. **Centralized API Services**

- Encapsulate API calls in reusable service modules:
  ```javascript
  import apiClient from './apiClient';

  export const fetchUsers = async () => {
    try {
      const response = await apiClient.get('/users');
      return response.data;
    } catch (error) {
      console.error('Error fetching users:', error);
      throw error;
    }
  };

  export const createUser = async (userData) => {
    try {
      const response = await apiClient.post('/users', userData);
      return response.data;
    } catch (error) {
      console.error('Error creating user:', error);
      throw error;
    }
  };
  ```

#### 4. **Error Handling**

- Use response interceptors for centralized error handling:
  ```javascript
  apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
      if (error.response) {
        switch (error.response.status) {
          case 400:
            console.error('Bad Request:', error.response.data);
            break;
          case 401:
            console.error('Unauthorized:', error.response.data);
            // Redirect to login if needed
            break;
          case 500:
            console.error('Server Error:', error.response.data);
            break;
          default:
            console.error('Unhandled Error:', error.response.data);
        }
      }
      return Promise.reject(error);
    }
  );
  ```

#### 5. **Testing and Debugging**

- Use **Postman** or **cURL** for initial API testing.
- Mock API calls during development and testing using:
  - **Mock Service Worker (MSW)** for frontend.
  - Custom mock data modules.
- Write unit tests for API services using Jest and mocking libraries like **axios-mock-adapter**.
  ```javascript
  import axios from 'axios';
  import MockAdapter from 'axios-mock-adapter';
  import { fetchUsers } from './apiService';

  const mock = new MockAdapter(axios);

  test('fetchUsers should return user data', async () => {
    const data = [{ id: 1, name: 'John Doe' }];
    mock.onGet('/users').reply(200, data);

    const result = await fetchUsers();
    expect(result).toEqual(data);
  });
  ```

---

### Standards and Best Practices

1. **Security**:
   - Use HTTPS for all API requests.
   - Avoid exposing sensitive data in the frontend.

2. **Consistency**:
   - Maintain a standardized API response structure (e.g., `{ data, error, message }`).

3. **Scalability**:
   - Use feature-based modules to organize services and ensure scalability as the application grows.

4. **Documentation**:
   - Document all APIs and their integration details using tools like Swagger or Postman.