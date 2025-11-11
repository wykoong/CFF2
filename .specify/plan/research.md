# Phase 0 — research.md
Generated: 2025-11-07

## Decision: Framework and libraries
- Decision: Use Python + Flask (minimal dependencies). Development/test-only tools: pytest, black, flake8, coverage.
- Rationale: User required minimal libraries and a small web stack; Flask + stdlib sqlite3 meets that while remaining easy to audit and test.
- Alternatives considered:
  - Django (too heavyweight)
  - Adding ORM (SQLAlchemy) — deferred to avoid extra dependency surface

## Decision: Data access & migrations
- Decision: Use sqlite3 from Python stdlib with a small DAO layer. Migrations implemented as ordered SQL scripts under
  .specify\db\migrations and a migrations table to record applied scripts.
- Rationale: Keeps toolchain minimal, portable, and auditable.
- Migration artifact: .specify\db\migrations\001_create_feedback_table.sql (see Phase 1)

## Decision: Frontend
- Decision: Vanilla HTML, CSS, JS for both public feedback form and operator portal. Progressive enhancement and accessible
  markup (labels, aria attributes).
- Rationale: Matches requirement to avoid frontend frameworks and keep UX simple and auditable.

## Decision: File/media handling
- Decision: DO NOT accept image uploads. Only store non-file metadata in sqlite (JSON text field).
- Rationale: Matches user constraint and reduces attack surface.

## Decision: Authentication for operator portal
- Decision: Implement simple session-based operator authentication using Flask sessions and password hashing via
  werkzeug.security (bundled with Flask). Credentials stored in an operators table (hashed).
- Rationale: Avoids adding extra authentication libraries while providing a secure-enough operator login for a small app.
- Alternatives considered:
  - External auth provider / SSO (better for larger orgs) — may be integrated later

## Decision: Audit & status workflow
- Decision: Record every operator action (accept/ignore/status changes) in an audit_trail table with actor id, action,
  timestamp, and optional note. Feedback status enum: Pending, Ignored, New, In Progress, Completed.
- Rationale: Needed for traceability and to satisfy Governance/Constitution requirements.

## Decision: Testing & CI
- Decision: Require unit tests for DAO and business logic (pytest), integration tests for API endpoints, and basic
  performance/response smoke tests. CI (GitHub Actions recommended) to run black, flake8, pytest, coverage.
- Rationale: Aligns with constitution principles (Code Quality, Testing Standards).

## Decision: Performance targets
- Decision: Document lightweight targets: submission round-trip < 2s typical; p95 API latency < 300ms in normal load.
- Rationale: Reasonable for a small Flask app; monitoring recommended once in production.

## Unknowns resolved (defaults chosen)
- Operator auth: session-based auth using Flask sessions (resolved).
- Retention policy: default policy set to "retain 2 years; operators may delete/anonymize per request"; configurable later.
- Export format: CSV accepted for operator exports.
