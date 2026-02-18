## 2026-02-18 - [Enhance Password Security and Protect PII]
**Vulnerability:** Weak user password requirements (min 6 chars) and unprotected PII endpoints (GET /users/).
**Learning:** Business logic for security (password validation) was only logging warnings instead of enforcing rules. GET endpoints for users were public, exposing PII without authentication.
**Prevention:** Strictly enforce password policies in the Service layer by raising ValidationErrors. Protect sensitive PII endpoints with administrative authentication dependencies.
