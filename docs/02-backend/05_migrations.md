# Migrations

## 1. Introduction

This document outlines the migration strategy and processes for managing database schema changes across all environments. It provides guidelines for creating, reviewing, and deploying migrations safely.

## 2. Migration Management

### 2.1 Migration Tools
- **Primary Tool**: Django Migrations
- **Additional Tools**:
  - Database backup tools
  - Schema comparison tools
  - Migration testing framework

### 2.2 Key Commands
```bash
# Generate migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations

# Squash migrations
python manage.py squashmigrations <app> <migration_name>

# Merge migrations
python manage.py makemigrations --merge
```

## 3. Migration Workflows

### 3.1 Development Workflow
1. **Branch Creation**
   - Create feature branch from main
   - Pull latest migration state

2. **Migration Development**
   ```bash
   # Create migration
   python manage.py makemigrations --name descriptive_name

   # Review migration file
   # Apply migration
   python manage.py migrate
   ```

3. **Testing**
   - Run migration tests
   - Verify data integrity
   - Test rollback procedure

4. **Code Review**
   - Submit PR with:
     - Migration files
     - Updated models
     - Test cases
     - Rollback plan

### 3.2 CI/CD Pipeline Integration
```yaml
migration_job:
  stages:
    - validate_migrations
    - backup_database
    - apply_migrations
    - verify_schema
    - rollback_on_failure
```

## 4. Best Practices

### 4.1 Migration File Guidelines
```python
# Good Example
from django.db import migrations, models

class Migration(migrations.Migration):
    atomic = True
    
    dependencies = [
        ('myapp', '0001_initial'),
    ]
    
    operations = [
        migrations.AddField(
            model_name='order',
            name='tracking_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
```

### 4.2 Data Migration Guidelines
```python
def migrate_data(apps, schema_editor):
    # Get historical model
    Order = apps.get_model('orders', 'Order')
    
    # Perform data migration
    for order in Order.objects.all():
        # Transform data
        order.save()

class Migration(migrations.Migration):
    dependencies = [...]
    
    operations = [
        migrations.RunPython(
            migrate_data,
            reverse_code=migrations.RunPython.noop
        ),
    ]
```

### 4.3 General Rules
1. **Atomic Changes**
   - One logical change per migration
   - Keep migrations focused and small

2. **Backwards Compatibility**
   - Support zero-downtime deployments
   - Plan for rollback scenarios
   - Test both forward and backward migrations

3. **Documentation**
   - Clear descriptive names
   - Comments for complex migrations
   - Update changelog

## 5. Advanced Migration Patterns

### 5.1 Zero-Downtime Migrations
```python
# Step 1: Add new field as nullable
migrations.AddField(
    model_name='order',
    name='new_field',
    field=models.CharField(null=True),
),

# Step 2: Deploy code that writes to both fields
# Step 3: Backfill data
# Step 4: Make field required
migrations.AlterField(
    model_name='order',
    name='new_field',
    field=models.CharField(null=False),
),
```

### 5.2 Large Table Migrations
```python
# Use database hints for large tables
class Migration(migrations.Migration):
    hints = {
        'model_name': {
            'operation_name': 'CREATE INDEX CONCURRENTLY'
        }
    }
```

## 6. Testing Strategy

### 6.1 Migration Tests
```python
from django.test import TestCase
from django.db.migrations.executor import MigrationExecutor

class TestMigrations(TestCase):
    @property
    def app(self):
        return apps.get_containing_app_config(type(self).__module__).name

    def setUp(self):
        executor = MigrationExecutor(connection)
        old_apps = executor.loader.project_state(('myapp', '0001')).apps
        
        # Set up test data
        self.Model = old_apps.get_model('myapp', 'MyModel')
        self.Model.objects.create(name='test')
        
        # Run migration
        executor.migrate([('myapp', '0002')])
        new_apps = executor.loader.project_state(('myapp', '0002')).apps
        self.Model = new_apps.get_model('myapp', 'MyModel')

    def test_migration(self):
        # Test migration results
        self.assertEqual(self.Model.objects.count(), 1)
```

## 7. Troubleshooting Guide

### 7.1 Common Issues
1. **Migration Conflicts**
   ```bash
   # Detect conflicts
   python manage.py showmigrations --plan
   
   # Resolve conflicts
   python manage.py makemigrations --merge
   ```

2. **Failed Migrations**
   ```bash
   # Check migration status
   python manage.py showmigrations
   
   # Reset failed migration
   python manage.py migrate myapp zero
   python manage.py migrate myapp
   ```

### 7.2 Recovery Procedures
1. **Database Backup**
   ```bash
   # Create backup before migrations
   pg_dump dbname > backup.sql
   
   # Restore if needed
   psql dbname < backup.sql
   ```

2. **Migration Rollback**
   ```bash
   # Rollback to specific migration
   python manage.py migrate myapp 0001
   ```

## 8. Production Deployment

### 8.1 Deployment Checklist
1. **Pre-deployment**
   - Backup database
   - Verify migration tests
   - Check dependencies
   - Review rollback plan

2. **Deployment**
   - Apply migrations in transaction
   - Monitor performance
   - Verify data integrity

3. **Post-deployment**
   - Verify application functionality
   - Monitor error rates
   - Keep backup for 24 hours

### 8.2 Emergency Procedures
```bash
# Quick rollback script
#!/bin/bash
set -e

echo "Starting emergency rollback..."
pg_restore -d $DB_NAME $BACKUP_FILE
python manage.py migrate myapp 0001
echo "Rollback completed"
```

## 9. Monitoring and Maintenance

### 9.1 Migration Metrics
- Migration duration
- Table locks duration
- Transaction log size
- Error rates
- Performance impact

### 9.2 Maintenance Tasks
```sql
-- Regular maintenance queries
ANALYZE table_name;
VACUUM ANALYZE table_name;
REINDEX TABLE table_name;
```

## 10. Documentation Requirements

### 10.1 Migration Documentation
```markdown
# Migration: 0002_add_tracking_number

## Description
Adds tracking number field to Order model

## Dependencies
- 0001_initial

## Changes
- Add VARCHAR(100) field 'tracking_number'
- Create index on tracking_number

## Rollback
- Remove tracking_number field
- Remove index

## Verification Steps
1. Check Order model has tracking_number
2. Verify index exists
3. Test order creation with tracking
```