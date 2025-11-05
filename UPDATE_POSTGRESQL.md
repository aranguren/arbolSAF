# Update PostgreSQL Database Password

## Current Status
✅ Environment files have been updated with new credentials
⚠️ PostgreSQL database password must be updated to match

---

## New Database Credentials

- **Username:** `arbolsaf_user` (renamed from `mypassword`)
- **Password:** `aONhuiKOud6cfqDOSKK1GKdASniuURAF`
- **Database:** `arbolsaf`

---

## Option 1: Using Docker (Recommended if using Docker Compose)

### Step 1: Connect to PostgreSQL Container

```bash
cd /home/user/arbolSAF/Despliegue

# Start containers if not running
docker-compose up -d db

# Connect to PostgreSQL
docker-compose exec db psql -U postgres -d arbolsaf
```

### Step 2: Update User and Password

In the PostgreSQL prompt, run these commands:

```sql
-- Rename user from 'mypassword' to 'arbolsaf_user'
ALTER USER mypassword RENAME TO arbolsaf_user;

-- Set new password
ALTER USER arbolsaf_user WITH PASSWORD 'aONhuiKOud6cfqDOSKK1GKdASniuURAF';

-- Verify the change
\du

-- Exit
\q
```

### Step 3: Restart Services

```bash
# Restart all services to use new credentials
docker-compose restart

# Check logs for any authentication errors
docker-compose logs -f web
```

---

## Option 2: Direct PostgreSQL Connection

### If PostgreSQL is running locally (not in Docker)

```bash
# Connect to PostgreSQL
psql -U postgres -d arbolsaf

# Or if postgres user requires sudo
sudo -u postgres psql -d arbolsaf
```

Then run the same SQL commands as above.

---

## Option 3: If User Doesn't Exist Yet

If the user `mypassword` doesn't exist, create the new user:

```sql
CREATE USER arbolsaf_user WITH PASSWORD 'aONhuiKOud6cfqDOSKK1GKdASniuURAF';
GRANT ALL PRIVILEGES ON DATABASE arbolsaf TO arbolsaf_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO arbolsaf_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO arbolsaf_user;
```

---

## Verification

### Test Database Connection

```bash
# Test connection with new credentials
psql -h localhost -U arbolsaf_user -d arbolsaf

# Or with Docker
docker-compose exec db psql -U arbolsaf_user -d arbolsaf
```

You should be prompted for the password. Enter:
```
aONhuiKOud6cfqDOSKK1GKdASniuURAF
```

If connection succeeds, the password update was successful!

---

## Troubleshooting

### Error: "role mypassword does not exist"
The old user doesn't exist. Use Option 3 to create the new user.

### Error: "authentication failed"
- Double-check you typed the password correctly
- Verify the password in `Despliegue/docker-env/web.env` matches what you set in PostgreSQL
- Check PostgreSQL logs: `docker-compose logs db`

### Error: "FATAL: password authentication failed"
The password in the environment file doesn't match PostgreSQL. Re-run the ALTER USER command.

---

## After Successful Update

1. ✅ Verify application can connect to database
2. ✅ Restart all services
3. ✅ Test login functionality
4. ✅ Delete NEW_CREDENTIALS.txt file

```bash
# Test application
python manage.py check
# Or with Docker
docker-compose exec web python manage.py check

# Delete credential file
rm NEW_CREDENTIALS.txt
rm credentials.txt  # if it exists
```

---

## Security Notes

- The old password `mypassword` is now invalid and cannot be used
- The new password is 32 characters of random alphanumeric characters
- Keep this password secure and never commit it to git
- `.env` files are now in `.gitignore` to prevent accidental commits

---

**Status:** Ready to update PostgreSQL
**Next:** Run the commands above, then proceed to verification
