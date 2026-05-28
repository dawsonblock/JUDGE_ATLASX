"""Phase 4: Verify and fix Alembic migration chain linearity."""
import os
from pathlib import Path

def check_migration_chain():
    """Verify all migrations have correct down_revision links."""
    migrations_dir = Path("backend/alembic/versions")
    if not migrations_dir.exists():
        print("❌ Migrations directory not found")
        return False
    
    migrations = sorted(migrations_dir.glob("*.py"))
    prev_revision = None
    issues = []
    
    for migration in migrations:
        content = migration.read_text()
        # Extract revision and down_revision
        revision_line = [l for l in content.split('\n') if l.startswith('revision =')]
        down_revision_line = [l for l in content.split('\n') if l.startswith('down_revision =')]
        
        if not revision_line or not down_revision_line:
            continue
            
        revision = revision_line[0].split("'")[1] if "'" in revision_line[0] else None
        down_rev = down_revision_line[0].split("'")[1] if "'" in down_revision_line[0] else None
        
        # Check chain continuity
        if prev_revision and down_rev != prev_revision:
            if down_rev != 'None':  # First migration can be None
                issues.append(f"❌ {migration.name}: down_revision mismatch")
                print(f"   Expected {prev_revision}, got {down_rev}")
        
        prev_revision = revision
    
    if issues:
        print(f"\n❌ Found {len(issues)} chain issues")
        return False
    else:
        print("✓ Migration chain is linear and properly linked")
        return True

if __name__ == "__main__":
    success = check_migration_chain()
    exit(0 if success else 1)
