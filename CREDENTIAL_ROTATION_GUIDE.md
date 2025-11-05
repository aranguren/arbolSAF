# 🔴 URGENT: Credential Rotation Guide

## ⚠️ Security Incident

**Date Identified:** 2025-11-05

Environment files containing sensitive credentials were previously committed to the git repository and are publicly exposed. **All credentials must be rotated immediately.**

---

## Exposed Credentials

The following credentials were committed to version control and **MUST BE CHANGED**:

1. **Django SECRET_KEY:** `S3cr3t_K#Key`
2. **Database Username:** `mypassword`
3. **Database Password:** `mypassword`
4. **Production server hostname:** `arbolsaf.denebinc.com`

### Risk Level: 🔴 CRITICAL

Anyone with access to the git repository history can:
- Forge Django session cookies and CSRF tokens
- Access the production database
- Impersonate users
- Compromise the entire application

---

## Immediate Actions Required

### Step 1: Generate New SECRET_KEY

**On your production server or secure machine:**

```bash
# Generate a new strong secret key
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**Update the SECRET_KEY in:**
- Production server: `/path/to/production/.env`
- Docker deployment: `/path/to/Despliegue/.env`

**Example:**
```env
SECRET_KEY=django-insecure-x&y9n_k%2m@a-fGh3!p#qRs5*tU7vWxYz...
```

---

### Step 2: Change Database Passwords

**A. Generate Strong Password**

```bash
# Generate a 32-character random password
openssl rand -base64 32
# Or use: pwgen -s 32 1
```

**B. Update PostgreSQL Password**

Connect to your PostgreSQL database:

```bash
# If using Docker
docker exec -it arbolsaf-db psql -U postgres

# Or directly
psql -U postgres
```

Run these SQL commands:

```sql
-- Change the database user password
ALTER USER mypassword WITH PASSWORD 'your-new-strong-password-here';

-- If you want to rename the user (recommended):
ALTER USER mypassword RENAME TO arbolsaf_user;
ALTER USER arbolsaf_user WITH PASSWORD 'your-new-strong-password-here';

-- Verify the change
\du
```

**C. Update Environment Files**

Update `Despliegue/docker-env/web.env`:

```env
DB_USER=arbolsaf_user
DB_PASSWORD=your-new-strong-password-here
```

Update `core/settings.py` if you have hardcoded values (you shouldn't).

---

### Step 3: Update Environment Files

**For each environment file, replace placeholder values:**

#### `.env` (root directory)
```env
DEBUG=False
SECRET_KEY=<paste-your-new-secret-key>
SERVER=your-actual-domain.com
```

#### `Despliegue/.env`
```env
DEBUG=False
SECRET_KEY=<paste-your-new-secret-key>
SERVER=arbolsaf.denebinc.com
```

#### `Despliegue/docker-env/web.env`
```env
SERVER=arbolsaf.denebinc.com
DB_HOST=db
DB_PORT=5432
DB_NAME=arbolsaf
DB_USER=arbolsaf_user
DB_PASSWORD=<paste-your-new-db-password>
```

---

### Step 4: Restart Services

**If using Docker:**

```bash
cd Despliegue
docker-compose down
docker-compose up -d

# Check logs for errors
docker-compose logs -f web
```

**If using systemd/other:**

```bash
# Restart your web server
sudo systemctl restart arbolsaf
# Or
sudo systemctl restart gunicorn
```

---

### Step 5: Invalidate All Sessions

After changing the SECRET_KEY, all existing sessions will be invalidated automatically. Users will need to log in again.

**Optionally, clear session table:**

```sql
-- Connect to database
psql -d arbolsaf -U arbolsaf_user

-- Clear all sessions
DELETE FROM django_session;
```

---

### Step 6: Remove Secrets from Git History

⚠️ **Warning:** This rewrites git history and requires force-push. Coordinate with your team first.

**Option A: Using git-filter-repo (Recommended)**

```bash
# Install git-filter-repo
pip install git-filter-repo

# Backup your repository first!
git clone /path/to/arbolSAF /path/to/arbolSAF-backup

# Remove sensitive files from history
git filter-repo --path .env --invert-paths
git filter-repo --path Despliegue/.env --invert-paths
git filter-repo --path Despliegue/docker-env/web.env --invert-paths
git filter-repo --path Despliegue/docker-env/pgadmin.env --invert-paths
git filter-repo --path Despliegue/docker-env/geoserver.env --invert-paths

# Force push to remote (requires coordination with team)
git push origin --force --all
git push origin --force --tags
```

**Option B: Using BFG Repo-Cleaner (Alternative)**

```bash
# Download BFG
wget https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar

# Backup first!
git clone --mirror /path/to/arbolSAF arbolSAF-backup.git

# Remove files
java -jar bfg-1.14.0.jar --delete-files '.env' arbolSAF.git
java -jar bfg-1.14.0.jar --delete-files '*.env' arbolSAF.git

cd arbolSAF.git
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push
git push --force
```

---

### Step 7: Notify Team Members

**Send this message to all developers:**

```
Subject: URGENT - Git History Contains Secrets - Action Required

Team,

We have identified that sensitive credentials were committed to our git
repository. The following actions have been taken:

1. All production credentials have been rotated
2. Environment files are now gitignored
3. Git history will be cleaned on [DATE]

ACTION REQUIRED FROM YOU:
- Pull the latest changes after [DATE/TIME]
- Delete your local repository and re-clone if you experience issues
- Update your local .env files with the new credentials (see wiki)
- Never commit .env files again

Questions? Contact [SECURITY LEAD]
```

---

## Verification Checklist

After completing all steps, verify:

- [ ] New SECRET_KEY is 50+ characters and unique
- [ ] Database password is 16+ characters with mixed case, numbers, symbols
- [ ] DEBUG=False in all production .env files
- [ ] All services restart successfully
- [ ] Users can log in (after re-authenticating)
- [ ] Database connections work
- [ ] `.env` files are in `.gitignore`
- [ ] No `.env` files in `git status`
- [ ] Team members notified
- [ ] Git history cleaned (optional but recommended)

---

## Testing After Rotation

```bash
# Test database connection
python manage.py dbshell

# Test Django settings
python manage.py check --deploy

# Test application start
python manage.py runserver

# Or with Docker
docker-compose up
```

---

## Additional Security Measures

### 1. Enable git-secrets

Prevent future credential leaks:

```bash
# Install git-secrets
brew install git-secrets  # macOS
# or
apt-get install git-secrets  # Ubuntu

# Setup in repository
cd /path/to/arbolSAF
git secrets --install
git secrets --register-aws  # Prevent AWS keys
git secrets --add 'SECRET_KEY.*'
git secrets --add 'PASSWORD.*'
git secrets --add 'DB_PASSWORD.*'

# Scan existing files
git secrets --scan
```

### 2. Use a Secrets Manager

For production, consider:
- **HashiCorp Vault**
- **AWS Secrets Manager**
- **Azure Key Vault**
- **Google Cloud Secret Manager**
- **1Password Secrets Automation**

### 3. Implement Pre-commit Hooks

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

# Check for .env files
if git diff --cached --name-only | grep -E "\.env$|\.env\..*$"; then
    echo "ERROR: Attempting to commit .env file!"
    echo "These files should never be committed."
    exit 1
fi

# Check for potential secrets
if git diff --cached | grep -E "SECRET_KEY|PASSWORD|API_KEY"; then
    echo "WARNING: Potential secret detected in commit"
    echo "Review carefully before proceeding"
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Incident Timeline

| Date | Event |
|------|-------|
| Unknown | `.env` files committed to repository |
| 2025-11-05 | Security audit identified exposed credentials |
| 2025-11-05 | `.env` files added to `.gitignore` |
| 2025-11-05 | Environment files updated with placeholder values |
| **[TODO]** | **Production credentials rotated** |
| **[TODO]** | **Git history cleaned** |
| **[TODO]** | **Team notified** |

---

## Support

If you encounter issues during rotation:

1. **Check logs:**
   ```bash
   # Django logs
   tail -f /var/log/arbolsaf/django.log

   # Docker logs
   docker-compose logs -f

   # PostgreSQL logs
   docker-compose logs db
   ```

2. **Common issues:**
   - **"Invalid SECRET_KEY"** - Ensure no extra spaces/newlines
   - **"Database authentication failed"** - Verify password was updated in both PostgreSQL AND .env
   - **"All sessions invalidated"** - Expected behavior, users must re-login

3. **Rollback plan:**
   - Keep backup of working `.env` files
   - Document current database credentials before changing
   - Test in staging environment first if possible

---

## Long-term Improvements

1. **Set up CI/CD secret scanning** (e.g., GitGuardian, TruffleHog)
2. **Implement automated secret rotation** (e.g., monthly)
3. **Use separate credentials** for each environment (dev/staging/prod)
4. **Enable database connection encryption** (SSL/TLS)
5. **Implement audit logging** for credential access
6. **Regular security training** for development team

---

## Questions or Issues?

Contact your security team or lead developer immediately if you:
- Cannot access production systems
- Encounter errors after rotation
- Notice suspicious activity
- Have questions about the process

**This is a critical security incident. Do not delay these actions.**

---

**Last Updated:** 2025-11-05
**Priority:** 🔴 CRITICAL
**Status:** ⚠️ CREDENTIALS NOT YET ROTATED
