# APPM (Application Portfolio Management) Module

## Overview

The APPM module provides comprehensive application portfolio management capabilities within NetBox. It allows organizations to track and manage their application landscape, including applications, servers, endpoints, and personnel.

## Models

### ApplicationGroup
Hierarchical grouping of applications with parent-child relationships.

**Key Features:**
- Tree structure with MPTT (Modified Preorder Tree Traversal)
- Unique naming constraints
- Support for nested organization

### Application
Core application entity with comprehensive metadata.

**Key Features:**
- Status tracking (active, deprecated, etc.)
- Version management
- Environment classification (production, staging, development)
- Criticality levels
- Owner and business unit assignment
- Tenant association
- Contact and image attachments support

### ApplicationServer
Physical or virtual servers hosting applications.

**Key Features:**
- Links to NetBox devices or virtual machines
- Resource tracking (CPU, memory, storage)
- Operating system and middleware information
- Role-based categorization
- Status management

### ApplicationEndpoint
Network endpoints and URLs for applications.

**Key Features:**
- URL and IP address management
- Protocol and port configuration
- SSL and authentication settings
- Load balancing indicators
- Health check URL tracking
- Public/private access flags

### ApplicationPersonnel
Personnel associated with applications.

**Key Features:**
- Role-based assignments
- Contact information management
- Primary and emergency contact designation
- Department and title tracking
- Start/end date management
- Integration with NetBox contacts

## API Endpoints

All models are fully accessible via REST API:

- `/api/appm/application-groups/`
- `/api/appm/applications/`
- `/api/appm/application-servers/`
- `/api/appm/application-endpoints/`
- `/api/appm/application-personnel/`

## Web Interface

The module provides complete web interface with:

- List views with filtering and search
- Detail views for each model
- Create/edit forms with validation
- Bulk import/export capabilities
- Integration with NetBox navigation

## Navigation

The APPM menu is organized into three groups:

1. **Applications**: Application Groups, Applications
2. **Infrastructure**: Application Servers, Application Endpoints  
3. **Personnel**: Application Personnel

## Search Integration

All models are indexed for NetBox's global search with appropriate field weighting:

- Names and descriptions have higher weight
- Secondary fields (versions, roles) have lower weight
- Related object names are searchable

## Permissions

Standard NetBox permissions apply:
- `appm.view_*` - View objects
- `appm.add_*` - Create objects
- `appm.change_*` - Modify objects
- `appm.delete_*` - Delete objects

## Usage Examples

### Creating an Application
1. Navigate to APPM > Applications > Applications
2. Click "Add" button
3. Fill required fields (name, environment)
4. Optionally assign to application group
5. Set status, version, and other metadata
6. Save

### Adding Application Servers
1. Create or select an application
2. Navigate to APPM > Infrastructure > Application Servers
3. Click "Add" and select the application
4. Link to existing device or virtual machine
5. Specify resources and configuration
6. Save

### Managing Endpoints
1. From application detail view, click "Add Endpoint"
2. Specify endpoint type (web, api, database, etc.)
3. Configure URL, IP, port as needed
4. Set security and access flags
5. Save

## Data Model Relationships

```
ApplicationGroup (tree structure)
    └── Application
        ├── ApplicationServer → Device/VirtualMachine
        ├── ApplicationEndpoint
        └── ApplicationPersonnel → Contact
```

## Validation Rules

- Application names must be unique within environment
- Server names must be unique within application
- Endpoint names must be unique within application
- Personnel name+role must be unique within application
- URLs must be valid format when provided
- Ports must be in valid range (1-65535)

## Integration Points

- **DCIM**: Links to devices for physical servers
- **Virtualization**: Links to virtual machines
- **Tenancy**: Tenant assignment and contact integration
- **Extras**: Custom fields, tags, and change logging
- **Core**: Full NetBox feature integration