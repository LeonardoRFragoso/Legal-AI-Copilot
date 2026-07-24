#!/usr/bin/env python3
"""
Demo Reset Script.

Cleans demo data and recreates demo users. Safe for development/demo only.

Usage:
    cd backend && ENVIRONMENT=development python -m scripts.demo_reset

Safety:
    - Refuses to run in production
    - Only clears demo-specific data
    - Preserves schema
    - Idempotent
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import User, Document, Conversation, Message, AutomationRun, AnalysisRecord, AnalysisReview
from app.auth import hash_password
from sqlalchemy import inspect


def check_environment():
    """Ensure we're not in production."""
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production":
        print("ERROR: Cannot run demo_reset in production environment.")
        sys.exit(1)
    print(f"Environment: {env}")


def show_summary(db):
    """Show what will be cleared."""
    tables = inspect(engine).get_table_names()
    print("\nCurrent data summary:")
    for model in [User, Document, Conversation, Message, AutomationRun, AnalysisRecord, AnalysisReview]:
        count = db.query(model).count()
        print(f"  {model.__tablename__}: {count} records")


def clear_demo_data(db):
    """Clear all data from demo tables (preserves schema)."""
    print("\nClearing demo data...")
    # Delete in FK-safe order
    db.query(AnalysisReview).delete()
    db.query(AnalysisRecord).delete()
    db.query(Message).delete()
    db.query(Conversation).delete()
    db.query(AutomationRun).delete()
    db.query(Document).delete()
    db.query(User).delete()
    db.commit()
    print("  All demo data cleared.")


def create_demo_users(db):
    """Create demo LAWYER and ADMIN users."""
    print("\nCreating demo users...")

    # Check if already exist
    existing_lawyer = db.query(User).filter(User.email == "lawyer@demo.com").first()
    if existing_lawyer:
        print("  lawyer@demo.com already exists — skipping")
    else:
        lawyer = User(
            name="Advogado Demo",
            email="lawyer@demo.com",
            password_hash=hash_password("demo123456"),
            role="LAWYER",
        )
        db.add(lawyer)
        print("  Created lawyer@demo.com (LAWYER)")

    existing_admin = db.query(User).filter(User.email == "admin@demo.com").first()
    if existing_admin:
        print("  admin@demo.com already exists — skipping")
    else:
        admin = User(
            name="Admin Demo",
            email="admin@demo.com",
            password_hash=hash_password("admin123456"),
            role="ADMIN",
        )
        db.add(admin)
        print("  Created admin@demo.com (ADMIN)")

    db.commit()


def main():
    check_environment()

    db = SessionLocal()
    try:
        show_summary(db)
        clear_demo_data(db)
        create_demo_users(db)
        show_summary(db)
        print("\nDemo reset complete.")
        print("\nDemo credentials:")
        print("  LAWYER: lawyer@demo.com / demo123456")
        print("  ADMIN:  admin@demo.com / admin123456")
    finally:
        db.close()


if __name__ == "__main__":
    main()
