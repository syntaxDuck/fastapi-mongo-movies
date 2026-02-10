## 2026-02-10 - [Critical] Plaintext Password Storage and Insecure Transmission
**Vulnerability:** Passwords were stored in plaintext and transmitted via URL query parameters in the POST /users/ endpoint.
**Learning:** The application had an incomplete architectural refactor where security "TODOs" were left in place while exposing the endpoint. The use of `Annotated[UserCreate, Query()]` in FastAPI specifically forced sensitive data into logs.
**Prevention:** Always use request bodies (not query parameters) for sensitive data. Never store passwords in plaintext; use at least PBKDF2 or a dedicated hashing library.
