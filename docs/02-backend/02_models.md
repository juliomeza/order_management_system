# Models

## Overview
This document focuses on the database models definition, detailing the core entities, their attributes, and relationships. The schema is designed to support multi-tenancy and RBAC while maintaining data integrity and efficiency.

## Core Entities

### 1. Core

#### Status
- **Columns:**
  - id (Primary Key)
  - name, description
  - code (Hierarchical structure)
  - statusType (Entity this status applies to)
  - isActive
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Centralized status management for all entities
- **Usage:** Used by multiple entities for state management

#### Types
- **Columns:**
  - id (Primary Key)
  - entity (The entity this type applies to)
  - typeName, description
  - isActive
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Flexible type management for various entities
- **Usage:** Generic type classification system

#### FeatureFlags
- **Columns:**
  - id (Primary Key)
  - name, description
  - isEnabled
  - scope (ENUM: global/customer/project)
  - scopeID (ID of customer/project if scoped)
  - createdDate, modifiedDate, createdBy, modifiedBy
- **Purpose:** Feature toggle management

#### Logs
- **Purpose:** History table for system activities
- **Columns:**
  - id (Primary Key)
  - entity (table name)
  - entityID
  - action (CREATE/UPDATE/DELETE)
  - details (JSON with before/after states)
  - timestamp
  - userID
- **Usage:** General activity logging, distinct from AuditLogs

#### AuditLogs
- **Columns:**
  - id (Primary Key)
  - entity (table name)
  - entityID
  - action (ENUM: CREATE/UPDATE/DELETE)
  - userID
  - timestamp
  - details (JSON with changes)
- **Purpose:** System-wide change tracking

### 2. Customers

#### Customers
- **Columns:**
  - id (Primary Key)
  - name
  - lookupCode (Unique)
  - statusID (Foreign Key to Status table)
  - addressID (Foreign Key to Addresses table)
  - outputFormat (ENUM: CSV, JSON)
  - notes
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Root entity for multi-tenant structure
- **Relationships:** One-to-many with Projects

#### Projects
- **Columns:**
  - id (Primary Key)
  - name, lookupCode (Unique)
  - ordersPrefix (Unique)
  - statusID (Foreign Key to Status table)
  - customerID (Foreign Key to Customers table)
  - notes
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Organize customer operations
- **Relationships:** Belongs to Customer, has many Users

#### Users
- **Columns:**
  - id (Primary Key)
  - firstName, lastName, username (Unique), email, password (hashed)
  - statusID (Foreign Key to Status table)
  - projectID (Foreign Key to Projects table)
  - roleID (Foreign Key to Roles table)
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Central user management for all system actors
- **Relationships:** Links to Projects and Roles

#### Roles
- **Columns:**
  - id (Primary Key)
  - roleName (e.g., SuperAdmin, ClientAdmin, Operator)
  - permissions (JSON field storing permitted actions)
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Define user access levels and capabilities

### 3. Inventory

#### Inventory
- **Columns:**
  - id (Primary Key)
  - projectID, warehouseID, materialID (Foreign Keys)
  - location, licensePlateID, licensePlate
  - lot, vendorLot
  - quantity
  - lastUpdated, updatedByUser
- **Purpose:** Track material quantities and locations
- **Relationships:** 
  - Links to Materials, Warehouses
  - One-to-many with InventorySerialNumbers

#### InventorySerialNumbers
- **Columns:**
  - id (Primary Key)
  - lookupCode (Serial number, unique)
  - statusID (Foreign Key to Status table)
  - licensePlateID (Foreign Key to Inventory)
  - notes
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Track individual serialized units within inventory
- **Relationships:** Belongs to specific Inventory record via licensePlateID

#### Materials
- **Columns:**
  - id (Primary Key)
  - lookupCode (Unique), name, description
  - projectID (Foreign Key to Projects)
  - statusID (Foreign Key to Status table)
  - type, isSerialized, price, uomID (Foreign Key to UOM)
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Product catalog management
- **Relationships:** Belongs to Project, references UOM

#### UOM (Units of Measure)
- **Columns:**
  - id (Primary Key)
  - name, lookupCode (Unique)
  - description
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Standardize unit measurements across the system
- **Relationships:** Referenced by Materials table

### 4. Orders

#### Orders
- **Columns:**
  - id (Primary Key)
  - lookupCodeOrder (Unique), lookupCodeShipment (Unique)
  - statusID (Foreign Key to Status table)
  - orderType (ENUM: 'INBOUND', 'OUTBOUND')
    - INBOUND: Receiving inventory into warehouse
    - OUTBOUND: Shipping inventory to customers
  - projectID, warehouseID, carrierID, serviceTypeID, addressID, billingID (Foreign Keys)
  - orderClassID (Foreign Key to OrderClasses)
  - expectedDeliveryDate
  - notes
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Core business transaction record
- **Relationships:** Links to multiple entities (Projects, Warehouses, Carriers, Addresses, OrderClasses)

#### OrderClasses
- **Columns:**
  - id (Primary Key)
  - className, description
  - isActive
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Categorize orders by type and processing rules
- **Relationships:** Referenced by Orders table

### 5. Logistics

#### Warehouses
- **Columns:**
  - id (Primary Key)
  - name, lookupCode (Unique)
  - addressID (Foreign Key to Addresses)
  - notes, statusID (Foreign Key to Status table)
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Physical location management
- **Relationships:** Has many Inventory records

#### Addresses
- **Columns:**
  - id (Primary Key)
  - addressLine1, addressLine2, city, state, country, postalCode
  - entityID (Polymorphic: customer/warehouse)
  - addressType (ENUM: shipping/billing)
  - notes, attentionOf
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Standardized address management
- **Relationships:** Used by multiple entities

#### Carriers
- **Columns:**
  - id (Primary Key)
  - name, lookupCode (Unique)
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Shipping provider management
- **Relationships:** Has many Services

#### CarrierServices
- **Columns:**
  - id (Primary Key)
  - name, lookupCode (Unique)
  - carrierID (Foreign Key to Carriers)
  - createdDate, modifiedDate, createdByUser, modifiedByUser
- **Purpose:** Specific shipping service options

## Database Optimization

### Indexes
1. **Primary Indexes:**
   - All `id` fields are primary keys
   - All `lookupCode` fields are unique indexes

2. **Foreign Key Indexes:**
   - All foreign key fields (ending in ID)
   - Composite indexes for frequently joined tables

3. **Performance Indexes:**
   - Inventory: (customerID, projectID, warehouseID, location)
   - Orders: (projectID, statusID, createdDate)
   - AuditLogs: (entity, entityID, timestamp)
   - InventorySerialNumbers: (lookupCode, licensePlateID)
   - Status: (code, statusType)
   - Types: (entity, typeName)

### Constraints
1. **Referential Integrity:**
   - All foreign keys have ON DELETE RESTRICT
   - Status changes follow valid state transitions
   - InventorySerialNumbers must reference valid Inventory records
   - Status codes must follow hierarchical structure
   - Order types must be valid ENUM values

2. **Business Rules:**
   - Order numbers must follow project prefix pattern
   - Inventory quantity cannot be negative
   - Users must have valid role assignments
   - Serial numbers must be unique within their scope
   - Status transitions must follow defined workflows
   - Type names must be unique within their entity context

## Notes
- All tables include standard audit fields (created/modified dates and users)
- Multi-tenancy enforced through customerID/projectID relationships
- Soft deletes implemented via statusID where applicable
- JSON fields used for flexible data storage (permissions, audit details)
- Serial number tracking implemented through InventorySerialNumbers relation
- Status and Types provide flexible state management
- Order types (inbound/outbound) determine workflow and validation rules