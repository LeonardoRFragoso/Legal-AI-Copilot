"""
Seed script for demo data.

Creates a LAWYER user and optionally an ADMIN user for demonstration.
Run: python -m app.seed
"""

from app.database import SessionLocal, engine, Base
from app.models import User, UserRole
from app.auth import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Create LAWYER user
        lawyer_email = "lawyer@demo.com"
        existing = db.query(User).filter(User.email == lawyer_email).first()
        if not existing:
            lawyer = User(
                name="Advogado Demo",
                email=lawyer_email,
                password_hash=hash_password("demo123456"),
                role=UserRole.LAWYER,
                is_active=True,
            )
            db.add(lawyer)
            print(f"Created LAWYER user: {lawyer_email} / demo123456")
        else:
            print(f"LAWYER user already exists: {lawyer_email}")

        # Create ADMIN user
        admin_email = "admin@demo.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            admin = User(
                name="Admin Demo",
                email=admin_email,
                password_hash=hash_password("admin123456"),
                role=UserRole.ADMIN,
                is_active=True,
            )
            db.add(admin)
            print(f"Created ADMIN user: {admin_email} / admin123456")
        else:
            print(f"ADMIN user already exists: {admin_email}")

        db.commit()
        print("\nSeed completed. Demo credentials:")
        print("  LAWYER: lawyer@demo.com / demo123456")
        print("  ADMIN:  admin@demo.com / admin123456")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
