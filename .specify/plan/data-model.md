# Phase 1 — data-model.md
Generated: 2025-11-07

## Entities

### Feedback
- Description: Stores a single feedback submission from a customer.
- Fields:
  - id: INTEGER PRIMARY KEY AUTOINCREMENT
  - email: TEXT NOT NULL
  - phone: TEXT NULLABLE
  - message: TEXT NOT NULL
  - status: TEXT NOT NULL DEFAULT 'Pending'  -- enum: Pending, Ignored, New, In Progress, Completed
  - metadata: TEXT NULLABLE -- JSON string (client locale, user agent, source)
  - created_at: TEXT NOT NULL -- ISO 8601
- Validation rules:
  - email: required, basic format validation
  - message: required, max length 5000
  - phone: optional, validate digits/format if provided

### Operator
- Description: Authenticated operator account for reviewing feedback.
- Fields:
  - id: INTEGER PRIMARY KEY AUTOINCREMENT
  - username: TEXT UNIQUE NOT NULL
  - password_hash: TEXT NOT NULL
  - display_name: TEXT NULLABLE
  - role: TEXT DEFAULT 'operator'
  - last_login: TEXT NULLABLE

### AuditTrail
- Description: Records operator actions on feedback items.
- Fields:
  - id: INTEGER PRIMARY KEY AUTOINCREMENT
  - feedback_id: INTEGER NOT NULL
  - operator_id: INTEGER NULLABLE
  - action: TEXT NOT NULL -- e.g., 'Accept', 'Ignore', 'Status:In Progress', 'Status:Completed'
  - note: TEXT NULLABLE
  - timestamp: TEXT NOT NULL

## Relationships
- Feedback (1) ← AuditTrail (many)
- Feedback (optional) ← assigned_operator_id (Operator) — optional assignment field if implemented

## Migrations
- .specify\db\migrations\001_create_feedback_table.sql — creates Feedback, Operator, AuditTrail, and migrations table
- Migration strategy: apply in order, record applied scripts in migrations table

## State transitions
- Initial: Pending
- Operator actions:
  - Ignore → Ignored (terminal)
  - Accept → New → In Progress → Completed
- Each transition creates an AuditTrail record with operator and timestamp
