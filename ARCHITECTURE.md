# Finance Tracker - Refactored Architecture

## Overview
The Finance Tracker application has been refactored from a monolithic Flask structure into a clean, layered architecture following MVC principles with proper separation of concerns.

## Architecture Layers

### 1. **Presentation Layer** (`app/views/`)
- **Purpose**: Handle HTTP requests and responses
- **Components**:
  - `auth_routes.py` - Authentication (login, register, logout)
  - `main_routes.py` - Dashboard, statistics, and API endpoints  
  - `transaction_routes.py` - Transaction management
  - `budget_routes.py` - Budget management
- **Responsibilities**:
  - Route handling and URL mapping
  - Request/response processing
  - Template rendering
  - Input validation

### 2. **Service Layer** (`app/services/`)
- **Purpose**: Business logic and domain operations
- **Components**:
  - `user_service.py` - User management and authentication logic
  - `transaction_service.py` - Transaction processing and financial calculations
  - `budget_service.py` - Budget operations and analytics
- **Responsibilities**:
  - Business rule enforcement
  - Data validation
  - Cross-cutting concerns (authorization, calculations)
  - Orchestration of repository operations

### 3. **Repository Layer** (`app/repositories/`)
- **Purpose**: Data access abstraction
- **Components**:
  - `base.py` - Abstract repository interface and database initialization
  - `user_repository.py` - User data operations
  - `transaction_repository.py` - Transaction data operations
  - `budget_repository.py` - Budget data operations
- **Responsibilities**:
  - Database CRUD operations
  - Query execution
  - Data mapping between database and models
  - Transaction management

### 4. **Domain Layer** (`app/models/`)
- **Purpose**: Core business entities and domain logic
- **Components**:
  - Data models: `User`, `Transaction`, `Budget`, `Category`
  - Value objects: `BudgetAnalytics`, `FinancialSummary`
  - Enums: `TransactionType`, `BudgetPeriod`
- **Responsibilities**:
  - Entity definitions
  - Domain validation
  - Business state management
  - Type safety

### 5. **Configuration Layer** (`config/`)
- **Purpose**: Application configuration and settings
- **Components**:
  - `settings.py` - Configuration management
- **Responsibilities**:
  - Environment-based configuration
  - Database connection settings
  - Application parameters

## Architecture Benefits

### **Separation of Concerns**
- Each layer has a single responsibility
- Business logic separated from data access and presentation
- Clean interfaces between layers

### **Testability**
- Repository pattern enables easy mocking
- Service layer can be unit tested independently
- Clear dependency injection points

### **Maintainability**
- Modular structure makes code easier to understand
- Changes in one layer don't affect others
- Easy to extend and modify

### **Scalability**
- Clear boundaries allow for easy refactoring
- Can switch databases without affecting business logic
- Can add new features without breaking existing code

### **Type Safety**
- Strongly typed models with dataclasses
- Enum usage for constants
- Better IDE support and error catching

## Design Patterns Used

### 1. **Repository Pattern**
- Abstracts data access logic
- Provides a consistent interface for data operations
- Enables easy testing with mock repositories

### 2. **Service Layer Pattern**
- Encapsulates business logic
- Provides a clear API for the presentation layer
- Handles transaction boundaries

### 3. **Factory Pattern** 
- Application factory (`create_app()`) for Flask initialization
- Centralized configuration and setup

### 4. **Blueprint Pattern**
- Modular route organization
- Clean URL structure
- Easy feature separation

## Database Schema
- **users**: User authentication and profile data
- **transactions**: Financial transactions with type support
- **budgets**: Budget allocations with period management
- **categories**: User-defined spending categories

## Running the Refactored Application

```bash
# Run the refactored version
python run_refactored.py

# Or run the original version for comparison
python app.py
```

## Migration Path
Both versions (original and refactored) work with the same database schema, allowing for seamless transition and comparison.

## Future Enhancements
With this architecture, the following can be easily added:
- Dependency injection container
- Async support
- Message queues for background processing
- Multiple database support
- API versioning
- Caching layer
- Event-driven architecture