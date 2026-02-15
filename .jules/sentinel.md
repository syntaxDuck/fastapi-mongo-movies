## 2026-02-11 - Insecure Password Handling and Transmission
**Vulnerability:** Passwords were being transmitted via URL query parameters and stored in plaintext in the database.
**Learning:** The use of `Annotated[UserCreate, Query()]` in FastAPI explicitly forced sensitive data into the URL, which is a common but dangerous pattern that leaks data to access logs and browser history. Missing hashing implementation left the database vulnerable.
**Prevention:** Always use `Body` for sensitive data in FastAPI (Pydantic models default to Body in POST if not specified otherwise, but being explicit or avoiding `Query()` is key). Implement PBKDF2 or similar robust hashing in the Service layer before data reaches the Repository.

## 2026-02-12 - NoSQL Injection in Repository Layer
**Vulnerability:** MongoDB operators were being dynamically constructed using f-strings from user-provided 'mod' parameters, allowing potential NoSQL injection even if partially validated in the service layer.
**Learning:** Defense in depth is critical. Even if the service layer validates input, the repository layer should still enforce its own strict whitelist of allowed operators to prevent bypasses or vulnerabilities introduced by future service changes.
**Prevention:** Always use a strict whitelist for any dynamic parts of a database query, such as operators or field names, at the lowest possible layer (Repository).

## 2026-02-15 - Enhanced Password Hashing and Timing Attack Protection
**Vulnerability:** Passwords were being hashed with 100,000 iterations (below OWASP 600k recommendation) using a fixed format that lacked algorithm agility, and verification used standard string comparison vulnerable to timing attacks.
**Learning:** Even if a hashing implementation exists, it must be periodically reviewed against current security standards. Implementing a versioned hash format (e.g., iterations\$salt\$hash) allows for seamless security upgrades without disrupting existing users.
**Prevention:** Use 'secrets.compare_digest' for all security-sensitive comparisons. Follow OWASP recommendations for PBKDF2 iterations (currently 600,000). Use a flexible hash storage format to allow for future parameter tuning.
