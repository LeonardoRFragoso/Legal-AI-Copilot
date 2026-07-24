#!/usr/bin/env python3
"""
Seed script to create test users with appropriate roles.
This script is idempotent and safe to run multiple times.

Usage:
    python seed_users.py

Environment variables:
    DATABASE_URL: SQLAlchemy database URL (optional, uses default from config)
"""

import os
import sys
from app.database import SessionLocal
from app.repositories import UserRepository
from app.auth import hash_password
from app.models import UserRole

# Test users to create
TEST_USERS = [
    {
        "name": "Admin User",
        "email": "admin@example.com",
        "password": "AdminPass123",
        "role": UserRole.ADMIN,
    },
    {
        "name": "Lawyer User",
        "email": "lawyer@example.com",
        "password": "LawyerPass123",
        "role": UserRole.LAWYER,
    },
    {
        "name": "Assistant User",
        "email": "assistant@example.com",
        "password": "AssistantPass123",
        "role": UserRole.ASSISTANT,
    },
    {
        "name": "Client User",
        "email": "client@example.com",
        "password": "ClientPass123",
        "role": UserRole.CLIENT,
    },
    {
        "name": "Viewer User",
        "email": "viewer@example.com",
        "password": "ViewerPass123",
        "role": UserRole.VIEWER,
    },
]


def seed_users():
    """Create test users if they don't already exist."""
    db = SessionLocal()
    user_repo = UserRepository(db)
    
    created_count = 0
    skipped_count = 0
    
    print("🌱 Seeding test users...\n")
    
    for user_data in TEST_USERS:
        email = user_data["email"]
        
        # Check if user already exists
        existing_user = user_repo.get_by_email(email)
        if existing_user:
            print(f"⏭️  Skipped: {email} (already exists)")
            skipped_count += 1
            continue
        
        # Create new user
        try:
            password_hash = hash_password(user_data["password"])
            user = user_repo.create(
                name=user_data["name"],
                email=email,
                password_hash=password_hash,
                role=user_data["role"],
            )
            print(f"✅ Created: {email} ({user_data['role'].value})")
            created_count += 1
        except Exception as e:
            print(f"❌ Error creating {email}: {str(e)}")
    
    db.close()
    
    print(f"\n📊 Summary:")
    print(f"   Created: {created_count}")
    print(f"   Skipped: {skipped_count}")
    print(f"\n✨ Seeding complete!")
    
    if created_count > 0:
        print(f"\n📝 Test credentials:")
        for user_data in TEST_USERS:
            if user_repo.get_by_email(user_data["email"]):
                print(f"   {user_data['email']} / {user_data['password']}")


if __name__ == "__main__":
    seed_users()
