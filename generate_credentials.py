#!/usr/bin/env python3
"""
Generate secure credentials for arbolSAF application
No Django dependency required
"""

import secrets
import string

def generate_secret_key(length=50):
    """Generate a Django-style SECRET_KEY"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(length))

def generate_password(length=32):
    """Generate a secure password"""
    # Use alphanumeric only for database password (safer for shell)
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))

if __name__ == '__main__':
    print("=" * 60)
    print("ARBOLSAF CREDENTIAL GENERATOR")
    print("=" * 60)
    print()

    secret_key = generate_secret_key()
    db_password = generate_password()

    print("1. NEW SECRET_KEY (copy this):")
    print("-" * 60)
    print(secret_key)
    print()

    print("2. NEW DATABASE PASSWORD (copy this):")
    print("-" * 60)
    print(db_password)
    print()

    print("=" * 60)
    print("WHAT TO DO NEXT:")
    print("=" * 60)
    print()

    print("Update these files with the values above:")
    print()
    print("File 1: .env")
    print("------")
    print(f"""DEBUG=False
SECRET_KEY={secret_key}
SERVER=127.0.0.1""")
    print()

    print("File 2: Despliegue/.env")
    print("------")
    print(f"""DEBUG=False
SECRET_KEY={secret_key}
SERVER=arbolsaf.denebinc.com""")
    print()

    print("File 3: Despliegue/docker-env/web.env")
    print("------")
    print(f"""SERVER=arbolsaf.denebinc.com
DB_HOST=db
DB_PORT=5432
DB_NAME=arbolsaf
DB_USER=arbolsaf_user
DB_PASSWORD={db_password}""")
    print()

    print("File 4: Update PostgreSQL")
    print("------")
    print("Connect to database and run:")
    print(f"""ALTER USER mypassword RENAME TO arbolsaf_user;
ALTER USER arbolsaf_user WITH PASSWORD '{db_password}';""")
    print()

    # Save to file
    with open('NEW_CREDENTIALS.txt', 'w') as f:
        f.write(f"CREDENTIAL ROTATION - Generated\n")
        f.write(f"=" * 60 + "\n\n")
        f.write(f"SECRET_KEY:\n{secret_key}\n\n")
        f.write(f"DB_PASSWORD:\n{db_password}\n\n")
        f.write(f"DB_USER:\narbolsaf_user\n\n")
        f.write("=" * 60 + "\n")
        f.write("DELETE THIS FILE AFTER USE!\n")

    print("=" * 60)
    print("✓ Credentials saved to: NEW_CREDENTIALS.txt")
    print("⚠ REMEMBER: Delete NEW_CREDENTIALS.txt after updating!")
    print("=" * 60)
