#!/bin/bash
# Final verification script for credential rotation
# Run this after updating PostgreSQL to verify everything works

set -e

echo "============================================================"
echo "CREDENTIAL ROTATION - FINAL VERIFICATION"
echo "============================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print success
success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Function to print error
error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to print warning
warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

echo "Running verification checks..."
echo ""

# Check 1: Environment files exist and have content
echo "1. Checking environment files..."
if [ -f ".env" ] && [ -s ".env" ]; then
    if grep -q "70vq4O5Lsgl9Z" .env; then
        success ".env has new SECRET_KEY"
    else
        error ".env does not have the new SECRET_KEY"
    fi
else
    error ".env file missing or empty"
fi

if [ -f "Despliegue/.env" ] && [ -s "Despliegue/.env" ]; then
    if grep -q "70vq4O5Lsgl9Z" Despliegue/.env; then
        success "Despliegue/.env has new SECRET_KEY"
    else
        error "Despliegue/.env does not have the new SECRET_KEY"
    fi
else
    error "Despliegue/.env file missing or empty"
fi

if [ -f "Despliegue/docker-env/web.env" ] && [ -s "Despliegue/docker-env/web.env" ]; then
    if grep -q "aONhuiKOud6cfqDOSKK1GKdASniuURAF" Despliegue/docker-env/web.env; then
        success "Despliegue/docker-env/web.env has new DB password"
    else
        error "Despliegue/docker-env/web.env does not have the new DB password"
    fi
else
    error "Despliegue/docker-env/web.env file missing or empty"
fi
echo ""

# Check 2: No placeholder values remain
echo "2. Checking for placeholder values..."
if grep -r "REPLACE-THIS" .env Despliegue/.env Despliegue/docker-env/web.env 2>/dev/null; then
    error "Placeholder values still present!"
else
    success "No placeholder values found"
fi
echo ""

# Check 3: DEBUG is False
echo "3. Checking DEBUG mode..."
if grep -q "DEBUG=False" .env; then
    success "DEBUG=False in .env"
else
    warning "DEBUG is not False in .env"
fi

if grep -q "DEBUG=False" Despliegue/.env; then
    success "DEBUG=False in Despliegue/.env"
else
    warning "DEBUG is not False in Despliegue/.env"
fi
echo ""

# Check 4: Git status
echo "4. Checking git status..."
if git status --porcelain | grep -E "\.env$|\.env\."; then
    warning ".env files appear in git status (this is OK if they're untracked)"
else
    success ".env files are not tracked by git"
fi
echo ""

# Check 5: .gitignore
echo "5. Checking .gitignore..."
if grep -q "^\.env$" .gitignore && grep -q "^\*\.env$" .gitignore; then
    success ".gitignore configured correctly"
else
    error ".gitignore may not be configured correctly"
fi
echo ""

# Check 6: Docker (if available)
echo "6. Checking Docker setup (if applicable)..."
if command -v docker-compose &> /dev/null; then
    cd Despliegue 2>/dev/null || true
    if [ -f "docker-compose.yml" ]; then
        if docker-compose config > /dev/null 2>&1; then
            success "Docker Compose configuration is valid"
        else
            error "Docker Compose configuration has errors"
        fi
    fi
    cd - > /dev/null 2>/dev/null || true
else
    warning "Docker Compose not available (skip if not using Docker)"
fi
echo ""

# Check 7: Credentials file cleanup
echo "7. Checking for credential files to delete..."
if [ -f "NEW_CREDENTIALS.txt" ]; then
    error "NEW_CREDENTIALS.txt still exists - DELETE IT!"
    echo "   Run: rm NEW_CREDENTIALS.txt"
else
    success "NEW_CREDENTIALS.txt has been deleted"
fi

if [ -f "credentials.txt" ]; then
    error "credentials.txt still exists - DELETE IT!"
    echo "   Run: rm credentials.txt"
else
    success "credentials.txt has been deleted (or never created)"
fi
echo ""

echo "============================================================"
echo "NEXT STEPS"
echo "============================================================"
echo ""
echo "If all checks passed above:"
echo ""
echo "1. Update PostgreSQL database password:"
echo "   See UPDATE_POSTGRESQL.md for instructions"
echo ""
echo "2. Test database connection:"
echo "   docker-compose exec db psql -U arbolsaf_user -d arbolsaf"
echo ""
echo "3. Restart services:"
echo "   docker-compose restart"
echo ""
echo "4. Verify application works:"
echo "   python manage.py check"
echo "   # Or: docker-compose exec web python manage.py check"
echo ""
echo "5. Test in browser:"
echo "   Navigate to your application and test login"
echo ""
echo "6. Delete credential files:"
echo "   rm NEW_CREDENTIALS.txt"
echo "   rm credentials.txt"
echo ""
echo "============================================================"
