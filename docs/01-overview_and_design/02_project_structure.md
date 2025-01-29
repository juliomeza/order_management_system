## Project Structure

order_management_system/
├── backend/
│   ├── manage.py                     # Main script for Django
│   ├── .env                          # Local environment variables
│   ├── .env.example                  # Template for environment variables
│   ├── .env.staging                  # Staging environment variables
│   ├── .env.production               # Production environment variables
│   ├── requirements/
│   │   ├── base.txt                  # Base dependencies
│   │   ├── local.txt                 # Development dependencies
│   │   └── production.txt            # Production dependencies
│   ├── config/
│   │   ├── asgi.py                   # ASGI configuration
│   │   ├── settings.py               # Base settings
│   │   ├── urls.py                   # Main URLs
│   │   └── wsgi.py                   # WSGI configuration
│   ├── apps/
│   │   ├── core/                     # Shared models
│   │   ├── customers/                # Customer-related functionality
│   │   │   ├── api/                  # API
│   │   │   │   ├── serializers/                    
│   │   │   │   ├── views/
│   │   │   │   ├── urls.py
│   │   │   │   └── filters.py
│   │   │   ├── services/             # Business logic
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── tests.py
│   │   │   ├── validators.py
│   │   │   └── views.py
│   │   ├── inventory/                # Inventory-specific logic
│   │   ├── orders/                   # Order-specific logic
│   │   └── logistics/                # Transportation-specific logic
│   ├── shared/
│   │   ├── auth/                     # Authentication and permissions
│   │   ├── middleware/               # Middleware logic
│   │   │   ├── multi_tenancy.py      # Middleware for customer data isolation
│   │   │   └── rbac.py               # Middleware for role-based access control
│   │   └── utils/                    # Utility functions
│   └── audit/
│       ├── handlers/
│       ├── formatters/
│       ├── middleware/
│       └── loggers/

├── frontend/
│   ├── .env                          # Local environment variables
│   ├── package.json                  # Dependencies
│   ├── vite.config.ts                # Vite configuration
│   ├── src/
│   │   ├── main.tsx                  # Main entry point
│   │   ├── App.tsx                   # Root component
│   │   ├── modules/
│   │   │   ├── customer-management/  # Customer management module
│   │   │   ├── order-processing/     # Order processing module
│   │   │   └── [other modules]
│   │   ├── shared/
│   │   │   ├── components/           # Reusable components
│   │   │   ├── hooks/                # Custom hooks
│   │   │   ├── utils/                # Helper functions
│   │   │   ├── constants/            # Centralized constants
│   │   │   └── helpers/              # HTTP and storage helpers
│   │   ├── styles/                   # Global styles
│   │   └── assets/                   # Static assets

├── tests/
│   ├── README.md                     # Testing strategy and usage
│   ├── unit/                         # Unit tests for backend/frontend
│   ├── integration/                  # Integration tests
│   ├── e2e/                          # End-to-end tests

├── docs/
│   ├── README.md                     # Navigation for documentation
│   ├── [backend, frontend, integration-specific docs]

├── scripts/
│   ├── setup.sh                      # Setup script
│   ├── deploy.sh                     # Deployment script

└── docker/
    ├── docker-compose.yml            # Docker Compose configuration
    ├── backend/
    │   └── Dockerfile                # Backend container
    └── frontend/
        └── Dockerfile                # Frontend container
