# Security Checklist

**Purpose:** Security patterns and common vulnerabilities to check during validation loops

**Created:** 2026-02-27 (from Feature 01 KAI-1 lessons learned)  
**Last Updated:** 2026-02-27

**Applicable Stages:**
- S7.P2: Feature QC Validation Loop
- S7.P3: Final Review (PR Validation Loop)
- S9.P2: Epic Validation Loop

---

## Overview

This checklist consolidates common security vulnerabilities and prevention patterns discovered during feature validation. Use this during validation rounds to systematically verify security measures.

**Origin:** Created after Feature 01 (KAI-1) discovered critical path traversal vulnerability in serve_image endpoint during S7.P2 Round 1 RESTART (rigorous validation).

---

## 1. Path Traversal Prevention (File Serving)

**Vulnerability:** User-controlled filename allows reading arbitrary files via "../" sequences

**Attack Example:**
```text
GET /temp_images/../../backend/src/llm_config.py
→ Reads API keys from config file
```

### Prevention Checklist:

When serving user-specified files (e.g., FileResponse, send_file, static files):

- [ ] **Filename validation:** Reject suspicious characters
  - Reject: "/", "\\", ".." (directory traversal)
  - Example: `if "/" in filename or "\\" in filename or ".." in filename: raise HTTPException(400)`

- [ ] **Path resolution to absolute path**
  - Convert to absolute path: `resolved_path = Path(allowed_dir) / filename).resolve()`
  - Purpose: Resolve all ".." and symbolic links

- [ ] **Boundary verification**
  - Verify resolved path starts with allowed directory
  - Example: `if not str(resolved_path).startswith(str(allowed_dir.resolve())): raise HTTPException(403)`

- [ ] **File existence check with proper 404**
  - Check `if not resolved_path.exists(): raise HTTPException(404)`
  - Return 404 (not 403) to avoid information disclosure

- [ ] **Security event logging**
  - Log attempted path traversal: `logger.warning(f"Path traversal attempt: {filename}")`
  - Include client IP if available for incident response

- [ ] **Media type determination from extension (not user input)**
  - Determine from file extension: `media_type = "image/jpeg" if ext == ".jpeg" else "image/png"`
  - Never trust `Content-Type` from user input

### Code Example (Correct Implementation):

```python
from pathlib import Path
from fastapi import HTTPException
from fastapi.responses import FileResponse

ALLOWED_DIR = Path("temp_images")

async def serve_file(filename: str):
    # 1. Filename validation
    if "/" in filename or "\\" in filename or ".." in filename:
        logger.warning(f"Path traversal attempt rejected: {filename}")
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    # 2. Path resolution
    resolved_path = (ALLOWED_DIR / filename).resolve()
    
    # 3. Boundary verification
    if not str(resolved_path).startswith(str(ALLOWED_DIR.resolve())):
        logger.error(f"Access denied outside {ALLOWED_DIR}: {resolved_path}")
        raise HTTPException(status_code=403, detail="Access denied")
    
    # 4. File existence check
    if not resolved_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # 5. Media type from extension
    media_type = "image/jpeg" if resolved_path.suffix == ".jpeg" else "image/png"
    
    # 6. Serve file
    return FileResponse(resolved_path, media_type=media_type)
```

---

## 2. Input Validation

**Vulnerability:** Unvalidated user input leads to injection attacks (SQL, NoSQL, Command)

### Prevention Checklist:

- [ ] **Use Pydantic models for API requests**
  - All API endpoints accept Pydantic models (not raw dicts)
  - Example: `async def endpoint(request: MyRequestModel):`

- [ ] **Validate string lengths**
  - min_length and max_length on all string fields
  - Example: `prompt: str = Field(..., min_length=1, max_length=2000)`

- [ ] **Validate numeric ranges**
  - Use `ge=0` (greater than or equal) for non-negative integers
  - Example: `seed: int = Field(..., ge=0)`

- [ ] **Use Literal types for enums**
  - Restrict to known values: `output_format: Literal["jpeg", "png"]`
  - Or use Python Enum with field_validator

- [ ] **Sanitize for specific contexts**
  - SQL: Use parameterized queries (never string concatenation)
  - Shell commands: Use `shlex.quote()` or avoid shell=True
  - HTML: Use template engine auto-escaping (React, Jinja2)

### SQL Injection Prevention:

❌ **NEVER DO THIS:**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

✅ **ALWAYS DO THIS:**
```python
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (username,))
```

### Command Injection Prevention:

❌ **NEVER DO THIS:**
```python
os.system(f"convert {user_filename} output.png")
```

✅ **ALWAYS DO THIS:**
```python
import subprocess
subprocess.run(["convert", user_filename, "output.png"], check=True)
```

---

## 3. Authentication & Authorization

**Vulnerability:** Missing or weak authentication allows unauthorized access

### Prevention Checklist:

- [ ] **API keys stored in environment variables**
  - Never hard-code API keys in source code
  - Use `os.environ.get("API_KEY")` or similar

- [ ] **API keys not logged**
  - Sensitive data redacted from logs
  - Example: `logger.info(f"API request to {url}")` (don't log headers)

- [ ] **API keys not returned in errors**
  - Error messages don't leak credentials
  - Generic errors for auth failures: "Authentication failed"

- [ ] **HTTPS in production**
  - API keys transmitted over HTTPS only
  - Set `secure=True` on cookies containing auth tokens

- [ ] **Authorization checks on protected endpoints**
  - Verify user has permission to access resource
  - Don't rely on client-side checks alone

---

## 4. Cross-Site Scripting (XSS) Prevention

**Vulnerability:** Unescaped user input rendered in HTML allows script injection

### Prevention Checklist:

- [ ] **Use frameworks with auto-escaping**
  - React: Auto-escapes by default in {} expressions
  - Jinja2: Auto-escapes by default with `{{ variable }}`

- [ ] **Never use dangerouslySetInnerHTML or |safe**
  - If absolutely necessary, sanitize with DOMPurify or bleach

- [ ] **Base64 images rendered in img tag (safe)**
  - Example: `<img src="data:image/png;base64,{base64_string}" />`
  - Browser treats as image data, not executable code

- [ ] **Content-Security-Policy headers**
  - Prevent inline scripts: `Content-Security-Policy: script-src 'self'`

---

## 5. Error Message Security

**Vulnerability:** Detailed error messages leak implementation details or sensitive data

### Prevention Checklist:

- [ ] **No stack traces to users**
  - Catch exceptions at API boundary
  - Log full stack trace internally
  - Return generic message to user: "An error occurred, please try again"

- [ ] **No file paths in error messages**
  - Don't expose: "Failed to read /var/www/app/config/secrets.yaml"
  - Instead: "Configuration error, please contact support"

- [ ] **No SQL queries in error messages**
  - Don't expose: "Error in query: SELECT * FROM users WHERE id=..."
  - Instead: "Database error occurred"

- [ ] **Consistent error messages for auth failures**
  - Don't differentiate "user not found" vs "wrong password"
  - Always: "Invalid credentials" (prevents username enumeration)

### Code Example (Correct):

```python
try:
    result = do_something()
except SpecificError as e:
    logger.error(f"Specific error: {e}", exc_info=True)  # Full detail logged
    raise HTTPException(
        status_code=500,
        detail="An error occurred while processing your request"  # Generic to user
    )
```

---

## 6. API Key Management

**Vulnerability:** API key compromise allows unauthorized access

### Prevention Checklist:

- [ ] **API keys in environment variables only**
  - Never commit to version control (.gitignore .env files)
  - Use `.env.example` with placeholder values

- [ ] **API key rotation plan**
  - Document how to rotate keys if compromised
  - Test key rotation process

- [ ] **Separate keys for dev/prod environments**
  - Development uses different keys than production
  - Key compromise in dev doesn't affect prod

- [ ] **Minimum privilege principle**
  - API keys have only necessary permissions
  - Separate read-only vs read-write keys

---

## 7. Dependency Security

**Vulnerability:** Outdated dependencies with known vulnerabilities

### Prevention Checklist:

- [ ] **Pin dependency versions**
  - `requirements.txt` or `pyproject.toml` with exact versions
  - Example: `requests==2.31.0` (not `requests>=2.0`)

- [ ] **Run security audits**
  - Python: `pip-audit` or `safety check`
  - npm: `npm audit`

- [ ] **Update dependencies regularly**
  - Monthly security update reviews
  - Test after updates

---

## 8. Rate Limiting & DoS Prevention

**Vulnerability:** No rate limiting allows resource exhaustion

### Prevention Checklist:

- [ ] **Timeouts on external API calls**
  - Set reasonable timeout: `requests.post(url, timeout=60)`
  - Prevent hanging on slow/unresponsive services

- [ ] **Timeouts on client requests**
  - Frontend: AbortController with timeout
  - Example: `setTimeout(() => controller.abort(), 65000)`

- [ ] **File upload size limits**
  - Restrict max file size to prevent disk exhaustion
  - Example: FastAPI `File(..., max_length=10_000_000)` (10MB)

- [ ] **Rate limiting on API endpoints**
  - Use middleware like `slowapi` (FastAPI) or `express rate-limit` (Express)

---

## Quick Security Review Checklist

Use this for validation loop security dimension check:

- [ ] **File serving:** Filename validation + path resolution + boundary check ✅
- [ ] **Input validation:** Pydantic models with length/range validation ✅
- [ ] **SQL/Command injection:** Parameterized queries, no string concatenation ✅
- [ ] **XSS:** Auto-escaping framework, no dangerouslySetInnerHTML ✅
- [ ] **API keys:** Environment variables, not hard-coded ✅
- [ ] **Error messages:** Generic to users, detailed internally ✅
- [ ] **Logging:** Sensitive data redacted ✅
- [ ] **Timeouts:** External API calls and client requests ✅
- [ ] **Dependencies:** Pinned versions, regular security audits ✅

---

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- CWE (Common Weakness Enumeration): https://cwe.mitre.org/
- Security by Design Principles: Least Privilege, Defense in Depth, Fail Securely

---

## Changelog

**2026-02-27:** Created from Feature 01 (KAI-1) lessons learned
- Added Path Traversal Prevention section (discovered in serve_image endpoint)
- Added quick checklist for validation loop security checks

