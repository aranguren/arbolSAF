# Credential Rotation Verification Guide

**Date:** 2025-11-05
**Status:** 🔄 CREDENTIALS ROTATED - VERIFICATION IN PROGRESS

---

## Completed Steps ✅

- ✅ SECRET_KEY rotated
- ✅ Database passwords changed

---

## Verification Checklist

Run through these checks to ensure the credential rotation was successful and the application is functioning properly.

---

## 1. Verify Django Configuration

### Check Django Settings
```bash
cd /home/user/arbolSAF

# Check that Django can load settings without errors
python manage.py check

# Check deployment readiness
python manage.py check --deploy
```

**Expected output:**
- No errors about missing SECRET_KEY
- System check should pass
- May show warnings about other security settings (expected)

**If you see errors:**
- "SECRET_KEY not set" → Check your .env file has SECRET_KEY=...
- "SECRET_KEY is weak" → Ensure you're not using the old exposed key

---

## 2. Verify Database Connection

### Test Database Access
```bash
# Test database connection
python manage.py dbshell
```

**In the PostgreSQL prompt, run:**
```sql
-- Test connection
SELECT current_database();
SELECT current_user;

-- Verify tables exist
\dt

-- Test a simple query
SELECT COUNT(*) FROM arbolsaf_species;

-- Exit
\q
```

**Expected:**
- Should connect without password errors
- Should show your database name
- Should list Django tables
- Should return species count

**If you see errors:**
- "authentication failed" → Password mismatch between .env and PostgreSQL
- "role does not exist" → Username was changed but not updated in .env
- Connection timeout → Check DB_HOST and DB_PORT in .env

---

## 3. Verify Migrations

### Check Migration Status
```bash
# Check if all migrations are applied
python manage.py showmigrations

# Look for [ ] (unapplied) vs [X] (applied)
```

**Expected:**
- All migrations should show [X] (applied)

**If migrations are unapplied:**
```bash
python manage.py migrate
```

---

## 4. Test Application Startup

### Development Server Test
```bash
# Start development server
python manage.py runserver 0.0.0.0:8000
```

**Expected:**
- Server starts without errors
- No SECRET_KEY warnings
- No database connection errors

**Access in browser:**
- Navigate to: http://localhost:8000
- Should load login page without errors

**Test login:**
- Try logging in with existing credentials
- Should work normally (sessions work with new SECRET_KEY)

**Press Ctrl+C to stop the server**

---

## 5. Verify Docker Deployment (If Using Docker)

### Test Docker Compose
```bash
cd /home/user/arbolSAF/Despliegue

# Check docker-compose configuration
docker-compose config

# Start services
docker-compose up -d

# Check logs for errors
docker-compose logs web
docker-compose logs db
```

**Expected:**
- No environment variable errors
- Web service starts successfully
- Database accepts connections
- No authentication failures

**Test web service:**
```bash
# Check if web service is responding
docker-compose exec web python manage.py check

# Test database connection from container
docker-compose exec web python manage.py dbshell
```

**If everything works:**
```bash
# Keep services running or stop them
docker-compose down
```

---

## 6. Verify Environment Files

### Check Environment Configuration

**Root .env:**
```bash
cat /home/user/arbolSAF/.env
```

**Expected content:**
```env
DEBUG=False
SECRET_KEY=django-insecure-<50+ character random string>
SERVER=your-domain.com
```

**Deployment .env:**
```bash
cat /home/user/arbolSAF/Despliegue/.env
```

**Docker web.env:**
```bash
cat /home/user/arbolSAF/Despliegue/docker-env/web.env
```

**Verify:**
- ✅ SECRET_KEY is 50+ characters and NOT the old exposed key
- ✅ SECRET_KEY is different from the examples
- ✅ DB_PASSWORD is NOT "mypassword"
- ✅ DEBUG=False in production environments
- ✅ No placeholder text like "REPLACE-THIS-SECRET-WAS-EXPOSED-IN-GIT"

---

## 7. Test Key Functionality

### Test User Authentication
```bash
# Create a test superuser (if needed)
python manage.py createsuperuser
```

**Test in browser:**
1. Navigate to login page
2. Log in with credentials
3. Access admin panel: http://localhost:8000/admin/
4. Navigate through the application
5. Test CRUD operations on species data

**Expected:**
- Login works normally
- Sessions persist
- CSRF protection works
- No security errors

---

## 8. Test Production Environment (If Applicable)

### Production Server Checks

**If deploying to production server:**

```bash
# SSH to production server
ssh user@arbolsaf.denebinc.com

# Navigate to application directory
cd /path/to/arbolsaf

# Pull latest changes
git pull origin claude/find-vulnerabilities-011CUqBpnBDXMR14XKiQHgmW

# Update environment files with new credentials
# (Do NOT commit these changes)
nano .env
nano Despliegue/.env
nano Despliegue/docker-env/web.env

# Restart services
sudo systemctl restart arbolsaf
# OR
docker-compose restart

# Check logs
sudo journalctl -u arbolsaf -f
# OR
docker-compose logs -f web

# Test the application
curl -I https://arbolsaf.denebinc.com
```

---

## 9. Verify Security Improvements

### Test DEBUG is Disabled

**Access a non-existent URL:**
- Navigate to: http://localhost:8000/this-page-does-not-exist

**Expected (DEBUG=False):**
- Generic 404 error page
- NO stack trace
- NO file paths or code snippets
- NO environment variables

**If you see detailed error page:**
- DEBUG is still enabled
- Check .env has DEBUG=False
- Restart application

### Test SQL Injection Fix

**Try filter with special characters:**
- Navigate to species list with filters
- Try: `/arbolsaf/especie/listado?tipo_variable=1'; DROP TABLE arbolsaf_species; --`

**Expected:**
- Should either:
  - Show normal results (if parameter is valid)
  - Show no results (if parameter is invalid)
  - Return error about invalid input
- Should NOT execute SQL injection
- Should NOT show SQL error with table names

---

## 10. Performance Check

### Verify No Performance Degradation

```bash
# Run a few queries
python manage.py shell
```

```python
from arbolsaf.models import SpeciesModel
import time

# Test query performance
start = time.time()
species = list(SpeciesModel.objects.all())
end = time.time()
print(f"Query took {end - start:.2f} seconds")
print(f"Found {len(species)} species")

# Exit
exit()
```

**Expected:**
- Similar performance to before
- No significant slowdown from parameterized queries

---

## Common Issues and Solutions

### Issue: "SECRET_KEY not set"
**Solution:**
```bash
# Check .env file exists and has SECRET_KEY
cat .env | grep SECRET_KEY

# If missing, generate new one
python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Add to .env
echo "SECRET_KEY=your-generated-key" >> .env
```

### Issue: "database authentication failed"
**Solution:**
```bash
# Verify password in .env matches PostgreSQL
cat Despliegue/docker-env/web.env | grep DB_PASSWORD

# Reset password in PostgreSQL
docker-compose exec db psql -U postgres
# ALTER USER your_user WITH PASSWORD 'your_password';
```

### Issue: "All users logged out"
**Explanation:**
- This is expected after SECRET_KEY rotation
- All existing sessions are invalidated
- Users need to log in again
- This is a security feature

### Issue: CSRF token errors
**Solution:**
```bash
# Clear browser cookies
# Or use incognito/private browsing window

# Verify CSRF middleware is enabled in settings.py
cat core/settings.py | grep CsrfViewMiddleware
```

---

## Final Verification Checklist

Mark each item as you verify:

### Environment Configuration
- [ ] .env file has new SECRET_KEY (not the exposed one)
- [ ] SECRET_KEY is 50+ characters long
- [ ] DEBUG=False in production .env files
- [ ] Database passwords updated in all .env files
- [ ] No placeholder text in .env files

### Database
- [ ] Can connect to database with new credentials
- [ ] Database queries work normally
- [ ] No authentication errors in logs

### Application
- [ ] `python manage.py check` passes
- [ ] Development server starts without errors
- [ ] Login functionality works
- [ ] Admin panel accessible
- [ ] CRUD operations work
- [ ] No detailed error pages (DEBUG=False verified)

### Docker (if applicable)
- [ ] Docker containers start successfully
- [ ] Web service connects to database
- [ ] No environment variable errors in logs
- [ ] Application accessible via Docker

### Production (if applicable)
- [ ] Production server updated
- [ ] Services restarted successfully
- [ ] Application accessible via domain
- [ ] SSL/HTTPS working
- [ ] No errors in production logs

### Security
- [ ] DEBUG disabled in production
- [ ] SQL injection attempts blocked
- [ ] Old SECRET_KEY no longer in use
- [ ] Old database passwords no longer work
- [ ] .env files not tracked by git

---

## Success Criteria

✅ **All checks passed** means your credential rotation is successful and the application is secure.

If any checks fail, refer to the troubleshooting sections in this guide or the CREDENTIAL_ROTATION_GUIDE.md

---

## Next Steps After Verification

Once all checks pass:

1. **Optional: Clean Git History**
   - See CREDENTIAL_ROTATION_GUIDE.md section 6
   - Removes exposed secrets from git history
   - Requires force push and team coordination

2. **Address Remaining Vulnerabilities**
   - Review SECURITY_VULNERABILITIES.md
   - Focus on High severity issues next
   - Plan remediation timeline

3. **Deploy to Production**
   - Merge PR to main branch
   - Deploy using standard process
   - Monitor for any issues

4. **Update Team**
   - Notify team about credential changes
   - Share new environment configuration
   - Remind about .gitignore changes

---

**Last Updated:** 2025-11-05
**Status:** 🔄 In Progress - Awaiting Verification Results
