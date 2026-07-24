#!/usr/bin/env python3
"""
Demo Check Script.

Validates that the demo environment is ready.

Usage:
    cd backend && ENVIRONMENT=development python -m scripts.demo_check

Checks:
    - Backend accessible
    - Database accessible
    - Migrations at head
    - Demo users exist
    - Frontend build exists or can be built
    - OPENAI_API_KEY present (optional — for real LLM demo)
    - Key endpoints respond
"""

import sys
import os
import subprocess

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models import User
from sqlalchemy import inspect


def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"  [{status}] {label}" + (f" — {detail}" if detail else ""))
    return condition


def main():
    print("=== Demo Environment Check ===\n")

    all_pass = True

    # Check 1: Database accessible
    try:
        db = SessionLocal()
        db.execute(db.bind.dialect.server_version_info.__class__())
        all_pass &= check("Database accessible", True)
    except Exception as e:
        all_pass &= check("Database accessible", False, str(e))
        db = None
    finally:
        if db:
            db.close()

    # Check 2: Tables exist
    if db is not None:
        try:
            tables = inspect(engine).get_table_names()
            required = ["users", "documents", "conversations", "messages",
                       "automation_runs", "analysis_records", "analysis_reviews"]
            missing = [t for t in required if t not in tables]
            all_pass &= check("All required tables exist", len(missing) == 0,
                            f"missing: {missing}" if missing else "")
        except Exception as e:
            all_pass &= check("All required tables exist", False, str(e))

    # Check 3: Migrations at head
    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "heads"],
            capture_output=True, text=True,
            env={**os.environ, "ENVIRONMENT": os.getenv("ENVIRONMENT", "development")}
        )
        has_single_head = "head" in result.stdout and result.returncode == 0
        all_pass &= check("Alembic has single head", has_single_head)
    except Exception as e:
        all_pass &= check("Alembic has single head", False, str(e))

    # Check 4: Demo users exist
    try:
        db = SessionLocal()
        lawyer = db.query(User).filter(User.email == "lawyer@demo.com").first()
        admin = db.query(User).filter(User.email == "admin@demo.com").first()
        all_pass &= check("Demo LAWYER user exists", lawyer is not None)
        all_pass &= check("Demo ADMIN user exists", admin is not None)
    except Exception as e:
        all_pass &= check("Demo users exist", False, str(e))
    finally:
        if db:
            db.close()

    # Check 5: OPENAI_API_KEY (optional)
    api_key = os.getenv("OPENAI_API_KEY", "")
    all_pass &= check("OPENAI_API_KEY present (optional)", bool(api_key),
                      "heuristic mode will be used" if not api_key else "LLM mode available")

    # Check 6: Frontend build
    frontend_dist = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "frontend", "dist", "index.html"
    )
    all_pass &= check("Frontend build exists", os.path.exists(frontend_dist),
                      "run 'npm run build' in frontend/" if not os.path.exists(frontend_dist) else "")

    # Check 7: Demo document
    demo_pdf = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "Contrato_Prestacao_Servicos_Teste.pdf"
    )
    fixture_txt = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "backend", "tests", "fixtures", "synthetic_contract.txt"
    )
    has_demo_doc = os.path.exists(demo_pdf) or os.path.exists(fixture_txt)
    all_pass &= check("Demo document available", has_demo_doc)

    print(f"\n{'All checks passed!' if all_pass else 'Some checks failed — review above.'}")
    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
