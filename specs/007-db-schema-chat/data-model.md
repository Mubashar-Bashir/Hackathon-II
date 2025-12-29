# Data Model: Phase III - Layer 1 Database Schema for Stateless Chat

## Entity: Conversation

### Fields
- **id**: UUID (Primary Key, default: uuid.uuid4)
- **title**: Optional[str], max_length=200
- **user_id**: UUID (Foreign Key to User, indexed, required for security)
- **created_at**: datetime (Auto-generated, indexed)
- **updated_at**: datetime (Auto-generated, indexed)

### Relationships
- **messages**: One-to-Many relationship to Message entity (cascade delete)

### Validation Rules
- user_id must reference a valid user
- title is optional but if provided must be <= 200 characters
- created_at and updated_at are automatically managed

### State Transitions
- Created when user starts a new conversation
- Updated when conversation metadata changes
- Deleted with all associated messages when user deletes conversation

## Entity: Message

### Fields
- **id**: UUID (Primary Key, default: uuid.uuid4)
- **role**: str (Enum: "user", "assistant", indexed, required)
- **content**: str (min_length=1, max_length=5000, required)
- **conversation_id**: UUID (Foreign Key to Conversation, indexed, required)
- **user_id**: UUID (Foreign Key to User, indexed, required for security)
- **created_at**: datetime (Auto-generated, indexed)
- **updated_at**: datetime (Auto-generated, indexed)

### Relationships
- **conversation**: Many-to-One relationship to Conversation entity

### Validation Rules
- role must be either "user" or "assistant"
- content must be 1-5000 characters
- conversation_id must reference a valid conversation
- user_id must match the conversation owner
- created_at and updated_at are automatically managed

### State Transitions
- Created when user or AI sends a message
- Updated when message content is edited (future feature)
- Deleted when parent conversation is deleted (cascading)

## Database Constraints

### Foreign Key Constraints
- Message.user_id → User.id (CASCADE on delete)
- Message.conversation_id → Conversation.id (CASCADE on delete)
- Conversation.user_id → User.id (RESTRICT on delete)

### Indexing Strategy
- Conversation.user_id (for user isolation queries)
- Conversation.created_at (for chronological ordering)
- Message.conversation_id (for conversation history retrieval)
- Message.user_id (for user isolation queries)
- Message.created_at (for chronological ordering)

## Security Considerations

### User Isolation
- All queries must filter by user_id to prevent cross-user data access
- Foreign key constraints enforce referential integrity
- Application logic must validate user_id matches authenticated user

### Data Integrity
- Cascading delete ensures consistency when conversations are removed
- Not-null constraints on required fields
- Check constraints on role field values

## API Contract Implications

### Query Patterns
- Get all conversations for a user (filter by user_id)
- Get all messages for a conversation (filter by conversation_id)
- Get conversation history with messages (JOIN query)
- Get recent messages for a user (filter by user_id, order by created_at)

### Performance Considerations
- Proper indexing for efficient conversation history retrieval
- UUID primary keys for distributed system compatibility
- Indexed foreign keys for join performance