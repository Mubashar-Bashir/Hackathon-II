# Specification Improvements for SDD (Spec-Driven Development)

## 1. Authentication System Specification Template

### 1.1 Password Hashing Requirements
- **Primary Method**: bcrypt with proper configuration
- **Fallback Method**: PBKDF2 if bcrypt fails to initialize
- **Password Length Limit**: 72 bytes maximum (bcrypt limitation)
- **Salt Strategy**: Automatic salt generation
- **Rounds**: Configurable (recommended: 12 rounds)
- **Error Handling**: Graceful fallback when bcrypt initialization fails

### 1.2 User Model Requirements
- **Fields**: email, name, password_hash, created_at, updated_at
- **Validation**:
  - Email format validation
  - Password length validation (1-72 characters)
  - Name length validation (optional, max 100 characters)
- **Database Constraints**: Unique email, proper indexing

### 1.3 API Endpoint Requirements
- **Register Endpoint**: POST /auth/register
  - Input: email, name, password
  - Output: user info and success message
  - Error Handling: Duplicate email, validation errors
- **Login Endpoint**: POST /auth/login
  - Input: email/username, password
  - Output: JWT token
  - Error Handling: Invalid credentials, rate limiting
- **Auth Middleware**: JWT token validation for protected routes

## 2. CORS Configuration Specification

### 2.1 Allowed Origins
- **Development**: http://localhost:3000, http://127.0.0.1:3000, http://0.0.0.0:3000
- **Environment Variable**: Configurable via environment variables
- **Production**: Configurable via environment variables

### 2.2 CORS Settings
- **Allow Credentials**: True
- **Allow Methods**: All methods (*)
- **Allow Headers**: All headers (*)
- **Regex Support**: For localhost variations

## 3. Notification System Specification

### 3.1 Task Model Requirements
- **Additional Fields**: reminder_sent (boolean, default: false)
- **Compatibility**: Both CLI and API models must be compatible
- **Conversion Layer**: Proper conversion between CLI and API models

### 3.2 Notification Endpoints
- **Check Due Tasks**: POST /tasks/notifications/check-due-tasks
- **Check Upcoming Tasks**: POST /tasks/notifications/check-upcoming-tasks?days=X
- **Authentication**: JWT token required
- **Response Format**: Consistent success/error format

## 4. Error Handling Specification

### 4.1 Password Hashing Errors
- **Bcrypt Initialization Failure**: Log warning, use fallback
- **Password Too Long**: Truncate to 72 characters before hashing
- **Verification Errors**: Proper error messages without revealing details

### 4.2 API Error Responses
- **Consistent Format**: { "detail": "error message" }
- **HTTP Status Codes**: Proper status codes for different error types
- **Logging**: All errors logged with appropriate severity

## 5. Testing Requirements

### 5.1 Unit Tests
- **Password Hashing**: Test both bcrypt and fallback methods
- **User Registration**: Test validation and error scenarios
- **Authentication**: Test login, logout, and token validation

### 5.2 Integration Tests
- **End-to-End Flow**: Registration → Login → API Access → Logout
- **CORS Testing**: Cross-origin request validation
- **Notification System**: End-to-end notification flow

### 5.3 E2E Tests (Playwright)
- **Authentication Flow**: Complete registration and login
- **Task Management**: Create, update, delete tasks
- **Error Scenarios**: Invalid credentials, network errors

## 6. Environment Configuration

### 6.1 Database Configuration
- **Development**: SQLite with file-based storage
- **Migration Strategy**: Clear migration path from dev to prod
- **Data Cleanup**: Procedures for test data management

### 6.2 Dependency Management
- **Version Compatibility**: Document working version combinations
- **Initialization Order**: Proper startup sequence for services
- **Fallback Mechanisms**: Graceful degradation when services fail

## 7. Monitoring and Observability

### 7.1 Logging Requirements
- **Authentication Events**: Log all auth attempts (success/failure)
- **Error Logging**: Detailed error information for debugging
- **Performance Logging**: Response times and resource usage

### 7.2 Health Checks
- **API Health**: /health endpoint for service status
- **Database Health**: Database connectivity check
- **External Services**: Notification service availability

## 8. Deployment Considerations

### 8.1 Configuration Management
- **Environment Variables**: All configurable settings via env vars
- **Secret Management**: Secure handling of sensitive data
- **Feature Flags**: Configurable feature toggles

### 8.2 Database Migrations
- **Schema Changes**: Proper migration procedures
- **Data Migration**: Procedures for existing user data
- **Rollback Strategy**: Ability to revert changes safely

## 9. SDD Implementation Checklist

Before starting any feature development, ensure:

### 9.1 Specification Completeness
- [ ] All technical requirements documented
- [ ] Error handling scenarios covered
- [ ] Security considerations addressed
- [ ] Performance requirements defined
- [ ] Testing requirements specified

### 9.2 Implementation Guidelines
- [ ] Code follows specification exactly
- [ ] Error handling implemented as specified
- [ ] Security measures implemented as specified
- [ ] Tests cover all specified scenarios
- [ ] Documentation updated

### 9.3 Quality Gates
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] All E2E tests pass
- [ ] Security scanning passes
- [ ] Performance benchmarks met

## 10. Lessons Learned from Current Issues

### 10.1 Password Hashing
- **Issue**: bcrypt initialization failures due to internal tests
- **Solution**: Always implement fallback mechanisms
- **Specification**: Include fallback strategy in requirements

### 10.2 Model Compatibility
- **Issue**: CLI and API models incompatibility
- **Solution**: Create conversion layer or unified models
- **Specification**: Define model compatibility requirements

### 10.3 CORS Configuration
- **Issue**: Missing notification endpoints in CORS
- **Solution**: Comprehensive CORS configuration
- **Specification**: List all required endpoints upfront

### 10.4 Database Consistency
- **Issue**: Schema changes breaking existing data
- **Solution**: Clear migration and cleanup procedures
- **Specification**: Include migration strategies in requirements