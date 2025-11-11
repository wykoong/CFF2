# Tasks: Customer Feedback Portal — add-feedback-portal

Feature dir: specs\1-add-feedback-portal  
Spec: specs\1-add-feedback-portal\spec.md  
Created: 2025-11-07

## Summary
- Total tasks: 30
- MVP suggested scope: User Story 1 (public submission flow) — tasks T012..T017
- Parallel opportunities: many frontend/backend tasks can run in parallel (marked [P])
- Independent test criteria: each user story phase includes an independent acceptance test that can be run against the deployed increment

---

## Phase 1 — Setup (project initialization)
Goal: Create repository layout, tooling, and migration scaffolding so implementation work can begin.

- [x] T001 [P] Create repository layout with directories: src/, templates/, static/js/, static/css/, tests/, .specify/db/migrations/ — path: (create) c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\
- [x] T002 [P] Add minimal dependency files: requirements-dev.txt and requirements.txt with flask, pytest, black, flake8 — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\requirements.txt
- [x] T003 [P] Create starter app entry file src/app.py with Flask app factory scaffold and blueprint registration (no implementation) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\app.py
- [x] T004 [P] Add database migrations directory and create initial migration file .specify/db/migrations/001_create_feedback_table.sql (schema for Feedback, Operator, AuditTrail) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\.specify\db\migrations\001_create_feedback_table.sql
- [x] T005 [P] Add basic README and quickstart snippet for local setup and migration apply commands — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\README.md
- [x] T006 [P] Create initial test runner configuration (pytest.ini) and placeholder test to validate test discovery — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\pytest.ini

## Phase 2 — Foundational (blocking prerequisites)
Goal: Implement reusable building blocks: DAO, models, migrations runner, auth, and templates layout.

- [x] T007 Implement DAO layer and DB helper using sqlite3: src/dao.py (functions: get_db, close_db, apply_migrations) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\dao.py
- [x] T008 Implement models/schema objects and enums for Feedback, Operator, AuditTrail: src/models.py — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\models.py
- [x] T009 Implement migrations runner script: scripts/run_migrations.py that applies SQL files from .specify/db/migrations — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\scripts\run_migrations.py
- [x] T010 Implement simple operator authentication helpers (password hashing and session helpers) in src/auth.py — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\auth.py
- [x] T011 Create HTML base templates and static asset placeholders:
        - templates/base.html
        - templates/public/feedback.html
        - templates/operator/login.html
        - templates/operator/dashboard.html
        — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\templates\

## Phase 3 — User Story 1 (P1) — Submit feedback (Customer)
Goal: Public form to submit feedback; server-side validation and persistence. Independent test: submit valid feedback and verify persisted record.

Independent test criteria:
- POST /api/feedback (or equivalent route) with valid payload returns 201 and record appears in DB with status=Pending.
- Invalid email => 400 and no DB record.

- [ ] T012 [US1] Implement POST /api/feedback endpoint handler (server-side validation and persistence) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\api\feedback.py
- [ ] T013 [P] [US1] Implement public feedback HTML form with client-side validation (email required, phone optional) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\templates\public\feedback.html
- [ ] T014 [P] [US1] Implement frontend JS to validate form and submit JSON to endpoint: static/js/feedback.js — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\static\js\feedback.js
- [ ] T015 [US1] Add unit tests for validation logic and DAO persistence: tests/test_feedback_submission.py — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\tests\test_feedback_submission.py
- [ ] T016 [US1] Add integration test that exercises the POST endpoint end-to-end against a test DB: tests/integration/test_feedback_api.py — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\tests\integration\test_feedback_api.py
- [ ] T017 [P] [US1] Add confirmation UI/response page and server-side flash/message on success: templates/public/feedback_success.html and update endpoint to redirect/render — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\templates\public\feedback_success.html

## Phase 4 — User Story 2 (P2) — Review and triage (Operator)
Goal: Authenticated operator can view submissions, filter by status, and Accept or Ignore. Independent test: operator logs in, views pending items, Accept/Ignore an item and verify audit entry and status change.

Independent test criteria:
- Unauthorized users cannot access operator endpoints.
- Operator can Accept -> status becomes New and AuditTrail entry created; can Ignore -> status Ignored and AuditTrail created.

- [ ] T018 [US2] Implement operator login endpoint and session handling (POST /operator/login) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\api\operator_auth.py
- [ ] T019 [US2] Implement operator dashboard endpoint GET /operator/feedback to list feedback with filters (status, date) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\api\operator_feedback.py
- [ ] T020 [P] [US2] Implement operator UI dashboard template with list, filter controls, and action buttons (Accept/Ignore) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\templates\operator\dashboard.html
- [ ] T021 [US2] Implement operator action endpoint POST /operator/feedback/{id}/action to Accept or Ignore and create AuditTrail record — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\api\operator_actions.py
- [ ] T022 [US2] Add tests for operator auth, list view access control, and Accept/Ignore action (unit + integration): tests/test_operator_flow.py — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\tests\test_operator_flow.py

## Phase 5 — User Story 3 (P3) — Work tracking (Operator)
Goal: Operators transition accepted feedback through New → In Progress → Completed; track operator and timestamps. Independent test: status transitions create AuditTrail entries and final Completed state persists.

Independent test criteria:
- Operator may change status in sequence and each change produces an audit record with operator id and timestamp.

- [ ] T023 [US3] Implement status transition logic and endpoint (part of operator_actions) supporting SetStatus with allowed transitions — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\api\operator_actions.py
- [ ] T024 [P] [US3] Add UI controls in operator dashboard for status transitions and internal notes: templates/operator/dashboard.html (update) and static/js/operator.js — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\static\js\operator.js
- [ ] T025 [US3] Add tests validating transition rules (cannot skip to Completed from Pending, audit entries created) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\tests\test_status_transitions.py
- [ ] T026 [US3] Implement optional assignment field and display of assignee in dashboard (DB schema and UI) — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\models.py and templates\operator\dashboard.html

## Phase 6 — Polish & Cross-Cutting Concerns
Goal: Add CI, linting, accessibility checks, export, docs, and contributor guidance.

- [ ] T027 [P] Add black and flake8 configuration files and pre-commit guidance: pyproject.toml and .flake8 — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\pyproject.toml
- [ ] T028 Add GitHub Actions workflow to run black --check, flake8, pytest, and coverage: .github/workflows/ci.yml — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\.github\workflows\ci.yml
- [ ] T029 [P] Implement CSV export endpoint/filter for operator exports and UI Export button: src/api/export.py and templates/operator/dashboard.html — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\src\api\export.py
- [ ] T030 Add CONTRIBUTING.md and update README with governance checks (lint/tests required, PR review rule) and accessibility checklist — path: c:\10_workplace\AI_SK_CustomerFeedbackForm\CFF2\CONTRIBUTING.md

---

## Dependencies & Order (high-level)
- Setup (T001..T006) MUST complete before Foundational (T007..T011).
- Foundational tasks (T007..T011) MUST complete before user story implementations (T012..T026).
- User Story order (recommended): US1 → US2 → US3 (but US2 and US3 can start after Foundational tasks; some UI/backend work is parallelizable).
- Polish tasks (T027..T030) can proceed in parallel with later story work but CI should be added early (T028 recommended as soon as tests exist).

## Parallel execution examples
- Example A: Backend developers implement T012, T007, T008, T009 in parallel with frontend dev implementing T013, T014, T017 (marked [P]).
- Example B: While US1 integration tests (T016) run, another developer implements operator login T018 and dashboard UI T020 in parallel.
- Example C: T027 (linters) and T028 (CI) can be implemented concurrently with any feature work.

## Task counts
- Total tasks: 30
- Setup tasks: 6
- Foundational tasks: 5
- US1 tasks: 6
- US2 tasks: 5
- US3 tasks: 4
- Polish tasks: 4

## Suggested MVP
- Implement Phase 1..3 (T001..T017) to deliver a working public feedback submission flow with persistence and confirmation.
- Rationale: Provides immediate user value and allows operator features to be built on top.

## Notes & Handoff
- Each task includes the exact file path where changes should be made.
- Tests are included for each story to allow independent verification of functionality.
- If authentication provider differs from the assumed simple session-based approach, update T010 and T018 accordingly before implementing operator flows.
