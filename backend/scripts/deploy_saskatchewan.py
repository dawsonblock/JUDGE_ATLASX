#!/usr/bin/env python3
"""
Saskatchewan Platform Deployment Scripts

This module provides easy-to-run scripts for deploying the public crime
understanding platform specifically for Saskatchewan.

Usage:
    python scripts/deploy_saskatchewan.py --step 1  # Apply migration
    python scripts/deploy_saskatchewan.py --step 2  # Load laws
    python scripts/deploy_saskatchewan.py --step 3  # Ingest Saskatoon data
    python scripts/deploy_saskatchewan.py --step 4  # Generate statute links
    python scripts/deploy_saskatchewan.py --step 5  # Generate summaries
"""

import asyncio
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

import sqlalchemy
from sqlalchemy import select, func
from sqlalchemy.orm import Session

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.db.session import get_async_session, engine
from app.models.entities import GeoLegalEvent, StatuteIncidentLink, LegalInstrument
from app.services.public_crime_statute_linker import CrimeStatuteLinker
from app.services.public_incident_explainer import IncidentExplainer


async def step_1_verify_migration():
    """Step 1: Verify database migration is applied."""
    print("[Step 1] Verifying database migration...")
    
    try:
        async with engine.begin() as conn:
            # Check if new tables exist
            tables = await conn.run_sync(
                lambda sync_conn: sync_conn.inspect().get_table_names()
            )
            
            required_tables = ["statute_incident_links", "incident_news_links"]
            missing = [t for t in required_tables if t not in tables]
            
            if missing:
                print(f"  ✗ Missing tables: {missing}")
                print(f"  Run: alembic upgrade head")
                return False
            
            print("  ✓ Database tables exist")
            print("  ✓ Migration verified successfully")
            return True
    except Exception as e:
        print(f"  ✗ Database connection failed: {e}")
        return False


async def step_2_load_saskatchewan_laws():
    """Step 2: Verify Saskatchewan statutes are loaded."""
    print("\n[Step 2] Verifying Saskatchewan statutes...")
    
    try:
        async with get_async_session() as session:
            # Count statutes by jurisdiction
            stmt = select(func.count()).select_from(LegalInstrument).where(
                LegalInstrument.jurisdiction == "CA-SK"
            )
            result = await session.execute(stmt)
            count = result.scalar()
            
            if count == 0:
                print("  ✗ No Saskatchewan statutes found")
                print("  Note: Statutes may need to be ingested separately")
                return False
            
            print(f"  ✓ Found {count} Saskatchewan statutes")
            
            # List key acts
            key_acts = [
                "Police Act",
                "Correctional Services Act",
                "Victims of Crime Act",
            ]
            
            for act in key_acts:
                stmt = select(func.count()).select_from(LegalInstrument).where(
                    (LegalInstrument.jurisdiction == "CA-SK")
                    & (LegalInstrument.law_title.contains(act))
                )
                result = await session.execute(stmt)
                act_count = result.scalar()
                status = "✓" if act_count > 0 else "○"
                print(f"  {status} {act}: {act_count} sections")
            
            return True
    except Exception as e:
        print(f"  ✗ Error checking statutes: {e}")
        return False


async def step_3_ingest_saskatoon_data():
    """Step 3: Ingest Saskatoon Police crime data."""
    print("\n[Step 3] Ingesting Saskatoon Police crime data...")
    
    try:
        from app.ingestion.crime_sources.saskatoon import import_saskatoon_csv
        
        fixture_path = (
            backend_path
            / "app/ingestion/crime_sources/fixtures/saskatoon_sample.csv"
        )
        
        if not fixture_path.exists():
            print(f"  ✗ Fixture file not found: {fixture_path}")
            return False
        
        print(f"  Reading fixture: {fixture_path}")
        
        with open(fixture_path, "r") as f:
            from app.db.session import SessionLocal
            db = SessionLocal()
            result = import_saskatoon_csv(db, f, commit=True)
            db.close()
        
        print(f"  ✓ Read {result.read_count} rows")
        print(f"  ✓ Persisted {result.persisted_count} incidents")
        if result.skipped_count:
            print(f"  ○ Skipped {result.skipped_count}")
        if result.error_count:
            print(f"  ✗ Errors: {result.error_count}")
            for error in result.errors[:5]:
                print(f"    - {error}")
        
        return result.error_count == 0
    except Exception as e:
        print(f"  ✗ Ingestion failed: {e}")
        return False


async def step_4_generate_statute_links():
    """Step 4: Generate statute links for Saskatoon incidents."""
    print("\n[Step 4] Generating statute links for Saskatoon incidents...")
    
    linker = CrimeStatuteLinker()
    
    try:
        async with get_async_session() as session:
            # Find all Saskatoon incidents
            stmt = select(GeoLegalEvent).where(
                GeoLegalEvent.jurisdiction == "Saskatchewan"
            )
            result = await session.execute(stmt)
            incidents = result.scalars().all()
            
            print(f"  Found {len(incidents)} Saskatoon incidents")
            
            if not incidents:
                print("  ○ No incidents found. Run step 3 first.")
                return False
            
            # Attempt to link first 5 for demonstration
            processed = 0
            succeeded = 0
            failed = 0
            
            for incident in incidents[:5]:
                try:
                    print(f"  Processing: {incident.title[:50]}...")
                    links = await linker.link_incident_to_statutes(
                        session=session,
                        incident_id=incident.id,
                        crime_type=incident.crime_type or "unknown",
                        description=incident.description or "",
                        location=incident.location_name or "Saskatoon, SK",
                    )
                    print(f"    ✓ Created {len(links)} statute links")
                    succeeded += 1
                except Exception as e:
                    print(f"    ✗ Error: {str(e)[:100]}")
                    failed += 1
                finally:
                    processed += 1
            
            print(f"\n  Results: {succeeded}/{processed} succeeded")
            if failed > 0:
                print(f"  Note: Some AI API calls may fail if ANTHROPIC_API_KEY not set")
            
            return failed == 0
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def step_5_generate_public_summaries():
    """Step 5: Generate public summaries for Saskatoon incidents."""
    print("\n[Step 5] Generating public summaries...")
    
    explainer = IncidentExplainer()
    
    try:
        async with get_async_session() as session:
            # Find incidents without summaries
            stmt = select(GeoLegalEvent).where(
                (GeoLegalEvent.jurisdiction == "Saskatchewan")
                & (GeoLegalEvent.public_summary == None)
            )
            result = await session.execute(stmt)
            incidents = result.scalars().all()
            
            print(f"  Found {len(incidents)} incidents without summaries")
            
            if not incidents:
                print("  ○ All incidents already have summaries")
                return True
            
            # Generate for first 3
            processed = 0
            succeeded = 0
            failed = 0
            
            for incident in incidents[:3]:
                try:
                    print(f"  Processing: {incident.title[:50]}...")
                    summary = await explainer.generate_public_summary(
                        session=session,
                        incident_id=incident.id,
                        incident_title=incident.title,
                        crime_type=incident.crime_type or "crime",
                        description=incident.description or "",
                        location=incident.location_name or "Saskatoon, SK",
                    )
                    incident.public_summary = summary
                    print(f"    ✓ Generated summary ({len(summary)} chars)")
                    succeeded += 1
                except Exception as e:
                    print(f"    ✗ Error: {str(e)[:100]}")
                    failed += 1
                finally:
                    processed += 1
            
            await session.commit()
            print(f"\n  Results: {succeeded}/{processed} succeeded")
            return failed == 0
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


async def run_all_steps():
    """Run all deployment steps in sequence."""
    print("=" * 60)
    print("JUDGE ATLAS - Saskatchewan Public Platform Deployment")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    steps = [
        ("Database Migration", step_1_verify_migration),
        ("Load Saskatchewan Laws", step_2_load_saskatchewan_laws),
        ("Ingest Saskatoon Data", step_3_ingest_saskatoon_data),
        ("Generate Statute Links", step_4_generate_statute_links),
        ("Generate Public Summaries", step_5_generate_public_summaries),
    ]
    
    results = []
    for name, step_func in steps:
        success = await step_func()
        results.append((name, success))
        
        if not success:
            print(f"\n✗ Deployment halted at: {name}")
            break
    
    print("\n" + "=" * 60)
    print("Deployment Summary")
    print("=" * 60)
    
    for name, success in results:
        status = "✓" if success else "✗"
        print(f"{status} {name}")
    
    all_success = all(success for _, success in results)
    
    if all_success:
        print("\n✓ Saskatchewan platform deployment complete!")
        print("\nNext steps:")
        print("1. Start the backend: uvicorn app.main:app --reload")
        print("2. Start the frontend: npm run dev")
        print("3. Visit http://localhost:3000/public/map")
    else:
        print("\n✗ Deployment incomplete. See errors above.")
    
    print("=" * 60)
    return all_success


def main():
    parser = argparse.ArgumentParser(
        description="Deploy Saskatchewan public crime platform"
    )
    parser.add_argument(
        "--step",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Run a specific step (1-5)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all steps in sequence",
    )
    
    args = parser.parse_args()
    
    if args.step:
        # Run specific step
        steps = {
            1: step_1_verify_migration,
            2: step_2_load_saskatchewan_laws,
            3: step_3_ingest_saskatoon_data,
            4: step_4_generate_statute_links,
            5: step_5_generate_public_summaries,
        }
        asyncio.run(steps[args.step]())
    else:
        # Run all steps
        asyncio.run(run_all_steps())


if __name__ == "__main__":
    main()
