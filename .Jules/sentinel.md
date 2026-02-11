## 2025-05-22 - Insecure Password Handling
**Vulnerability:** Passwords were being transmitted via URL query parameters and stored in plaintext.
**Learning:** FastAPI endpoints using `Annotated[BaseModel, Query()]` will expose all model fields (including passwords) in the URL.
**Prevention:** Use request bodies for sensitive data and always hash passwords in the service layer using PBKDF2-SHA256 before repository storage.
