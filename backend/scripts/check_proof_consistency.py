"""Check proof consistency for public platform.

Verifies that:
- No hardcoded status strings remain
- All responses use proper schemas
- Release policy is enforced
- No false production-ready claims
"""

import re
import sys
from pathlib import Path


def check_hardcoded_statuses(backend_dir: Path) -> list[str]:
    """Find remaining hardcoded status strings."""
    issues = []
    
    # Check for hardcoded review status strings
    for py_file in backend_dir.rglob("*.py"):
        if "test" in str(py_file) or "__pycache__" in str(py_file):
            continue
        
        content = py_file.read_text()
        
        # Look for hardcoded "pending", "approved", etc.
        if re.search(r'review_status\s*=\s*["\'](?:pending|approved|rejected)["\']', content):
            issues.append(f"❌ {py_file}: Hardcoded review_status string")
        
        if re.search(r'link_method\s*=\s*["\'](?:manual|ai|auto)["\']', content):
            issues.append(f"❌ {py_file}: Hardcoded link_method string")
    
    return issues


def check_schemas_used(backend_dir: Path) -> list[str]:
    """Check that public API endpoints use response schemas."""
    issues = []
    
    public_platform = backend_dir / "app/api/routes/public_platform.py"
    if not public_platform.exists():
        issues.append(f"❌ public_platform.py not found")
        return issues
    
    content = public_platform.read_text()
    
    # Check that schemas are imported
    if "PublicMapIncidentsResponse" not in content:
        issues.append("❌ PublicMapIncidentsResponse not imported")
    if "PublicIncidentWithLinks" not in content:
        issues.append("❌ PublicIncidentWithLinks not imported")
    
    # Check that endpoints return schemas
    if "return PublicMapIncidentsResponse" not in content:
        issues.append("❌ map endpoint doesn't return PublicMapIncidentsResponse")
    
    return issues


def check_release_policy_used(backend_dir: Path) -> list[str]:
    """Check that release policy is actually used."""
    issues = []
    
    public_platform = backend_dir / "app/api/routes/public_platform.py"
    if not public_platform.exists():
        return issues
    
    content = public_platform.read_text()
    
    # Check that policy is imported and used
    if "PublicReleasePolicy" not in content:
        issues.append("❌ PublicReleasePolicy not imported")
    if "is_incident_publicly_releasable" not in content:
        issues.append("❌ is_incident_publicly_releasable not called")
    if ".filter(" in content and "PublicReleasePolicy" not in content:
        issues.append("❌ Filter logic but no release policy check")
    
    return issues


def check_false_claims_removed(repo_root: Path) -> list[str]:
    """Check that false production-ready claims are removed."""
    issues = []
    
    files_to_check = [
        "README_PLATFORM.md",
        "PUBLIC_PLATFORM_README.md",
        "PRODUCTION_DEPLOYMENT.md",
    ]
    
    for filename in files_to_check:
        filepath = repo_root / filename
        if not filepath.exists():
            continue
        
        content = filepath.read_text()
        
        # Check for false claims
        if re.search(r"Production-Ready\s*✓", content):
            issues.append(f"❌ {filename}: Contains 'Production-Ready ✓'")
        if re.search(r"100%\s*Complete", content):
            issues.append(f"❌ {filename}: Contains '100% Complete'")
        if re.search(r"Ready to deploy\s*[!✓]", content, re.IGNORECASE):
            issues.append(f"❌ {filename}: False deployment readiness claim")
    
    return issues


def main():
    """Run all checks."""
    repo_root = Path(__file__).parent.parent.parent
    backend_dir = repo_root / "backend" / "app"
    
    print("=" * 60)
    print("PROOF CONSISTENCY CHECKS")
    print("=" * 60)
    
    all_issues = []
    
    print("\n1. Checking for hardcoded status strings...")
    issues = check_hardcoded_statuses(backend_dir)
    if issues:
        all_issues.extend(issues)
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   ✓ No hardcoded status strings found")
    
    print("\n2. Checking that response schemas are used...")
    issues = check_schemas_used(backend_dir)
    if issues:
        all_issues.extend(issues)
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   ✓ Response schemas properly imported and used")
    
    print("\n3. Checking that release policy is enforced...")
    issues = check_release_policy_used(backend_dir)
    if issues:
        all_issues.extend(issues)
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   ✓ Release policy is imported and used")
    
    print("\n4. Checking for false production-ready claims...")
    issues = check_false_claims_removed(repo_root)
    if issues:
        all_issues.extend(issues)
        for issue in issues:
            print(f"   {issue}")
    else:
        print("   ✓ No false production-ready claims found")
    
    print("\n" + "=" * 60)
    if all_issues:
        print(f"FAILED: {len(all_issues)} issues found")
        return 1
    else:
        print("PASSED: All consistency checks passed")
        return 0


if __name__ == "__main__":
    sys.exit(main())
