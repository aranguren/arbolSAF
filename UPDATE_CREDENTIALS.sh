#!/bin/bash
# Script to help update credentials in environment files
# Run this script to generate new credentials and see where to place them

set -e

echo "========================================="
echo "Credential Rotation Helper Script"
echo "========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed"
    exit 1
fi

# Generate new SECRET_KEY
echo "1. Generating new SECRET_KEY..."
echo ""
NEW_SECRET_KEY=$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
echo "   Generated SECRET_KEY:"
echo "   $NEW_SECRET_KEY"
echo ""

# Generate new database password
echo "2. Generating new database password..."
echo ""
if command -v openssl &> /dev/null; then
    NEW_DB_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
else
    # Fallback if openssl not available
    NEW_DB_PASSWORD=$(python3 -c "import secrets; import string; print(''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32)))")
fi
echo "   Generated Database Password:"
echo "   $NEW_DB_PASSWORD"
echo ""

echo "========================================="
echo "FILES TO UPDATE"
echo "========================================="
echo ""

# Check which environment files exist
echo "Environment files found:"
echo ""

if [ -f ".env" ]; then
    echo "✓ .env (root directory)"
fi

if [ -f "Despliegue/.env" ]; then
    echo "✓ Despliegue/.env"
fi

if [ -f "Despliegue/docker-env/web.env" ]; then
    echo "✓ Despliegue/docker-env/web.env"
fi

if [ -f "Despliegue/docker-env/pgadmin.env" ]; then
    echo "✓ Despliegue/docker-env/pgadmin.env"
fi

echo ""
echo "========================================="
echo "STEP-BY-STEP INSTRUCTIONS"
echo "========================================="
echo ""

echo "STEP 1: Update .env (root directory)"
echo "--------------------------------------"
echo "Edit file: .env"
echo ""
echo "Replace with:"
echo "DEBUG=False"
echo "SECRET_KEY=$NEW_SECRET_KEY"
echo "SERVER=127.0.0.1"
echo ""
echo "Command to update:"
echo "cat > .env << 'EOF'"
echo "DEBUG=False"
echo "SECRET_KEY=$NEW_SECRET_KEY"
echo "SERVER=127.0.0.1"
echo "EOF"
echo ""

echo "STEP 2: Update Despliegue/.env"
echo "--------------------------------------"
echo "Edit file: Despliegue/.env"
echo ""
echo "Replace with:"
echo "DEBUG=False"
echo "SECRET_KEY=$NEW_SECRET_KEY"
echo "SERVER=arbolsaf.denebinc.com"
echo ""
echo "Command to update:"
echo "cat > Despliegue/.env << 'EOF'"
echo "DEBUG=False"
echo "SECRET_KEY=$NEW_SECRET_KEY"
echo "SERVER=arbolsaf.denebinc.com"
echo "EOF"
echo ""

echo "STEP 3: Update Despliegue/docker-env/web.env"
echo "--------------------------------------"
echo "Edit file: Despliegue/docker-env/web.env"
echo ""
echo "Replace with:"
echo "SERVER=arbolsaf.denebinc.com"
echo "DB_HOST=db"
echo "DB_PORT=5432"
echo "DB_NAME=arbolsaf"
echo "DB_USER=arbolsaf_user"
echo "DB_PASSWORD=$NEW_DB_PASSWORD"
echo ""
echo "Command to update:"
echo "cat > Despliegue/docker-env/web.env << 'EOF'"
echo "SERVER=arbolsaf.denebinc.com"
echo "DB_HOST=db"
echo "DB_PORT=5432"
echo "DB_NAME=arbolsaf"
echo "DB_USER=arbolsaf_user"
echo "DB_PASSWORD=$NEW_DB_PASSWORD"
echo "EOF"
echo ""

echo "STEP 4: Update PostgreSQL Database Password"
echo "--------------------------------------"
echo "Connect to PostgreSQL and run:"
echo ""
echo "# If using Docker:"
echo "docker-compose exec db psql -U postgres -d arbolsaf"
echo ""
echo "# Then run these SQL commands:"
echo "ALTER USER mypassword RENAME TO arbolsaf_user;"
echo "ALTER USER arbolsaf_user WITH PASSWORD '$NEW_DB_PASSWORD';"
echo "\q"
echo ""

echo "========================================="
echo "QUICK UPDATE OPTION"
echo "========================================="
echo ""
echo "Want to update all files automatically? (y/n)"
read -p "> " answer

if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
    echo ""
    echo "Updating environment files..."

    # Update .env
    cat > .env << EOF
DEBUG=False
SECRET_KEY=$NEW_SECRET_KEY
SERVER=127.0.0.1
EOF
    echo "✓ Updated .env"

    # Update Despliegue/.env
    mkdir -p Despliegue
    cat > Despliegue/.env << EOF
DEBUG=False
SECRET_KEY=$NEW_SECRET_KEY
SERVER=arbolsaf.denebinc.com
EOF
    echo "✓ Updated Despliegue/.env"

    # Update Despliegue/docker-env/web.env
    mkdir -p Despliegue/docker-env
    cat > Despliegue/docker-env/web.env << EOF
SERVER=arbolsaf.denebinc.com
DB_HOST=db
DB_PORT=5432
DB_NAME=arbolsaf
DB_USER=arbolsaf_user
DB_PASSWORD=$NEW_DB_PASSWORD
EOF
    echo "✓ Updated Despliegue/docker-env/web.env"

    echo ""
    echo "========================================="
    echo "✓ Environment files updated successfully!"
    echo "========================================="
    echo ""
    echo "IMPORTANT: You still need to update PostgreSQL!"
    echo ""
    echo "Run these commands:"
    echo "docker-compose exec db psql -U postgres -d arbolsaf"
    echo ""
    echo "Then in PostgreSQL:"
    echo "ALTER USER mypassword RENAME TO arbolsaf_user;"
    echo "ALTER USER arbolsaf_user WITH PASSWORD '$NEW_DB_PASSWORD';"
    echo "\q"
    echo ""
    echo "After updating PostgreSQL, restart services:"
    echo "docker-compose restart"
    echo ""
else
    echo ""
    echo "No problem! Update the files manually using the commands above."
    echo ""
fi

echo "========================================="
echo "Credentials saved to: credentials.txt"
echo "========================================="
echo ""

# Save credentials to file for reference
cat > credentials.txt << EOF
CREDENTIAL ROTATION - $(date)
========================================

NEW SECRET_KEY:
$NEW_SECRET_KEY

NEW DATABASE PASSWORD:
$NEW_DB_PASSWORD

DATABASE USER:
arbolsaf_user

========================================
IMPORTANT: Delete this file after updating all systems!
Run: rm credentials.txt
========================================
EOF

echo "Your new credentials have been saved to credentials.txt"
echo "REMEMBER: Delete credentials.txt after you've updated everything!"
echo ""
echo "To verify the updates worked, run:"
echo "python manage.py check"
echo ""
