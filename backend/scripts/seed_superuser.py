"""
Database seeding script to create initial superuser.

This script creates a superuser account for initial system access.
Run this script to seed the database with a default superuser.
"""

from sqlalchemy.orm import Session
from database.session import SessionLocal
from database.auth import User
from authentication.utils.password_utils import hash_password


def seed_superuser():
    """Create initial superuser account."""
    
    db: Session = SessionLocal()
    
    try:
        # Check if superuser already exists
        existing_user = db.query(User).filter(User.username == "elaine.maua").first()
        
        if existing_user:
            print("⚠️  Superuser 'elaine.maua' already exists!")
            print(f"   User ID: {existing_user.id}")
            print(f"   Email: {existing_user.email}")
            print(f"   Active: {existing_user.is_active}")
            return
        
        # Hash the password
        password = "password123"
        password_hash = hash_password(password)
        
        # Create superuser
        superuser = User(
            firstname="Elaine",
            lastname="Maua",
            username="elaine.maua",
            email="elaine.maua@slotmein.com",
            user_role="superuser",
            pwd_hash=password_hash,
            is_active=True
        )
        
        db.add(superuser)
        db.commit()
        db.refresh(superuser)
        
        print("✅ Superuser created successfully!")
        print(f"   Username: {superuser.username}")
        print(f"   Password: {password}")
        print(f"   Name: {superuser.firstname} {superuser.lastname}")
        print(f"   Role: {superuser.user_role}")
        print(f"   Active: {superuser.is_active}")
        print(f"   User ID: {superuser.id}")
        print("\n🔐 You can now login with these credentials!")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating superuser: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🌱 Seeding database with superuser...")
    print("-" * 50)
    seed_superuser()
    print("-" * 50)
