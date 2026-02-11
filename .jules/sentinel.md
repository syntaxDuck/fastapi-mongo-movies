## 2026-02-11 - Insecure Password Handling and Transmission
**Vulnerability:** Passwords were being transmitted via URL query parameters and stored in plaintext in the database.
**Learning:** The use of `Annotated[UserCreate, Query()]` in FastAPI explicitly forced sensitive data into the URL, which is a common but dangerous pattern that leaks data to access logs and browser history. Missing hashing implementation left the database vulnerable.
**Prevention:** Always use `Body` for sensitive data in FastAPI (Pydantic models default to Body in POST if not specified otherwise, but being explicit or avoiding `Query()` is key). Implement PBKDF2 or similar robust hashing in the Service layer before data reaches the Repository.
