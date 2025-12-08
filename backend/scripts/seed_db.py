"""
Simple database seeding script - Run with: python -m backend.scripts.seed_db
"""

def seed_superuser():
    from database.session import SessionLocal
    from database.auth import User
    from authentication.utils.password_utils import hash_password
    
    db = SessionLocal()
    
    try:
        # Check if user exists
        existing = db.query(User).filter(User.username == "elaine.maua").first()
        if existing:
            print(f"⚠️  User 'elaine.maua' already exists (ID: {existing.id})")
            return
        
        # Create superuser
        password_hash = hash_password("password123")
        
        user = User(
            firstname="Elaine",
            lastname="Maua",
            username="elaine.maua",
            email="elaine.maua@slotmein.com",
            user_role="superuser",
            pwd_hash=password_hash,
            is_active=True
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        print("✅ Superuser created!")
        print(f"   Username: elaine.maua")
        print(f"   Password: password123")
        print(f"   ID: {user.id}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_superuser()
