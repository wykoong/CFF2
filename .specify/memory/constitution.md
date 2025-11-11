<!--
Sync Impact Report
- Version change: TODO(previous_version) -> 1.0.0
- Modified / Added principles:
  - Added: Code Quality → "Code Quality"
  - Added: Testing Standards → "Testing Standards"
  - Added: User Experience Consistency → "User Experience Consistency"
  - Added: Performance Requirements → "Performance Requirements"
- Added sections:
  - Governance: Amendment procedure, Versioning policy, Compliance review expectations
- Removed sections: none
- Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending — align "Constitution Check" items to require linting, test coverage, UX checklist, performance budgets
  - .specify/templates/spec-template.md: ⚠ pending — add mandatory sections for acceptance tests, performance criteria, UX consistency notes
  - .specify/templates/tasks-template.md: ⚠ pending — add task categories for observability, performance testing, UX review
  - .specify/templates/commands/*.md: ⚠ pending — scan for agent-specific names and replace with generic guidance where required
  - README.md: ⚠ pending — update governance summary and link to constitution
  - docs/quickstart.md: ⚠ pending — ensure quickstart includes required checks (linters, test runner, performance smoke tests)
- Follow-up TODOs:
  - TODO(RATIFICATION_DATE): original adoption date unknown — please supply YYYY-MM-DD
  - TODO(previous_version): prior constitution version unknown — verify and replace in report if available
  - Manual review required for each template file listed above; automated edits were not performed by this change
-->

# Project Constitution

Version: 1.0.0
Ratification date: TODO(RATIFICATION_DATE)
Last amended: 2025-11-07

## Preamble

This Constitution defines the core engineering, quality, user experience, and performance principles that govern
development, review, and release of the AI SK CustomerFeedbackForm project. These principles are normative: they
establish MUST/SHOULD obligations and the process for amendment and compliance review.

## Principles

### 1. Code Quality
Project artifacts MUST adhere to a shared code-quality baseline:
- All source code MUST pass the project's configured linters and formatters on CI.
- Changes to production code MUST be reviewed via pull request by at least one maintainer other than the author.
- Dependencies MUST be reviewed for security and license compatibility before upgrade; critical-security updates
  MUST be applied within a timebox defined by vulnerability severity.
Rationale: Consistent, reviewable code reduces defects, prevents regressions, and makes the codebase maintainable.

### 2. Testing Standards
Testing is mandatory and measurable:
- Unit tests MUST cover new and changed modules; core modules SHOULD target a minimum of 80% line coverage.
- Integration and end-to-end tests MUST be included for public APIs and user flows affected by a change.
- All tests MUST run in CI with each merge; failing tests block merges unless the failure is explicitly triaged
  and documented in the PR.
- Performance-sensitive changes MUST include automated performance tests or benchmarks demonstrating no
  regressions against defined budgets.
Rationale: Explicit, automated testing ensures reliability and supports safe change and refactoring.

### 3. User Experience Consistency
User-facing behavior and design MUST be consistent and accessible:
- Visual and interaction patterns MUST follow the project's design system or documented component library.
- All user-facing changes MUST include copy review and accessibility checks; accessibility baseline is WCAG 2.1 AA.
- UX changes SHOULD be accompanied by a usability note in the spec/PR describing impact, fallback behavior,
  and any roll-back plan.
Rationale: Predictable, accessible UX reduces user friction and supports inclusive product quality.

### 4. Performance Requirements
Performance constraints are first-class requirements:
- The project MUST define performance budgets for critical user journeys (examples: initial render,
  API p95 latency).
- New features MUST be evaluated against these budgets; changes that exceed budgets MUST include mitigation plans.
- Performance monitoring and alerting MUST be in place for production systems; critical regressions MUST be
  addressed as high-priority issues.
Rationale: Explicit budgets and monitoring prevent performance erosion and ensure acceptable user experience.

## Governance

### Amendment procedure
- Any contributor MAY propose an amendment by opening a PR that changes this file and includes:
  - A clear description of the change and rationale.
  - The intended version bump (major/minor/patch) with justification.
  - A proposed migration or compliance plan if the amendment introduces new obligations.
- Amendments require approval by at least two maintainers. Once merged, LAST_AMENDED is updated to the merge date.
- For breaking governance changes (principle removals or redefinitions), a public notice and a 14-day feedback period
  MUST be observed prior to merge.

### Versioning policy
- Versioning follows semantic rules for governance text:
  - MAJOR: Backwards-incompatible governance changes (principle removal or fundamental redefinition).
  - MINOR: Addition of new principles or expansion of normative guidance that increases obligations.
  - PATCH: Editorial changes, clarifications, or typo fixes.
- This document's Version line MUST be updated to reflect the new semantic version on amendment.

### Compliance review expectations
- Each release cycle SHOULD include a constitution compliance checklist verifying:
  - CI enforces linters and test runs.
  - New specs include performance/UX acceptance criteria when applicable.
  - Required templates and checklists were updated for any new obligations.
- Non-compliance findings MUST be triaged and tracked; high-risk gaps MUST be remediated before major releases.

## Signatures

Approved by maintainers:
- (maintainer-1) — TODO: add signature or GitHub handle
- (maintainer-2) — TODO: add signature or GitHub handle
