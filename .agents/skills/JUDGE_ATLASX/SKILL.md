```markdown
# JUDGE_ATLASX Development Patterns

> Auto-generated skill from repository analysis

## Overview
This skill guide covers the core development conventions and workflows for the JUDGE_ATLASX TypeScript codebase. It outlines file organization, coding style, and the main workflow for generating proof and status artifacts. This guide is designed to help contributors quickly understand and follow the established patterns in the repository.

## Coding Conventions

### File Naming
- **Style:** Snake case  
  **Example:**  
  ```
  user_profile.ts
  proof_batch_generator.ts
  ```

### Imports
- **Style:** Relative imports  
  **Example:**  
  ```typescript
  import { validateProof } from './proof_utils';
  import { getStatus } from '../status/status_checker';
  ```

### Exports
- **Style:** Named exports  
  **Example:**  
  ```typescript
  // In proof_utils.ts
  export function validateProof(data: any): boolean { ... }
  export const PROOF_VERSION = '1.0.0';
  ```

### Commit Messages
- **Pattern:** Freeform, no strict prefixes
- **Average Length:** ~65 characters  
  **Example:**  
  ```
  Update proof batch generation to include audit chain logs
  ```

## Workflows

### Proof Batch Generation
**Trigger:** When you need to snapshot and document the current proof, status, and readiness of the system (e.g., after a major change, repair, or before a release).  
**Command:** `/generate-proof-batch`

**Step-by-step Instructions:**
1. **Run system proof and validation processes.**
   - Execute scripts or commands that validate the current state of the backend, frontend, and system proofs.
2. **Generate logs for backend, frontend, and various checks.**
   - Collect logs such as `backend_compile.log`, `frontend_build.log`, and `verify_audit_chain.log`.
3. **Produce summary JSON and markdown files for status and readiness.**
   - Generate files like `release_readiness.md`, `proof_manifest.json`, and `source_registry_status.json`.
4. **Archive all generated artifacts under a timestamped directory.**
   - Store all outputs in a new folder under `artifacts/history/proof/<timestamp>/`.

**Files Involved:**
- `artifacts/history/proof/*/CURRENT_ALPHA_STATUS.md`
- `artifacts/history/proof/*/PROOF_POLICY.md`
- `artifacts/history/proof/*/SOURCE_REGISTRY_STATUS.md`
- `artifacts/history/proof/*/archive_validation.log`
- `artifacts/history/proof/*/archive_validation.md`
- `artifacts/history/proof/*/backend_compile.log`
- `artifacts/history/proof/*/backend_pytest.log`
- `artifacts/history/proof/*/backend_proof_summary.json`
- `artifacts/history/proof/*/frontend_build.log`
- `artifacts/history/proof/*/frontend_typecheck.log`
- `artifacts/history/proof/*/release_readiness.md`
- `artifacts/history/proof/*/release_gate.json`
- `artifacts/history/proof/*/proof_manifest.json`
- `artifacts/history/proof/*/source_registry_status.json`
- `artifacts/history/proof/*/verify_audit_chain.log`

**Example Directory Structure:**
```
artifacts/
  history/
    proof/
      2024-06-15T12-30-00Z/
        CURRENT_ALPHA_STATUS.md
        PROOF_POLICY.md
        ...
```

## Testing Patterns

- **Framework:** Unknown (not detected)
- **File Pattern:** Test files are named with `.test.` in the filename  
  **Example:**  
  ```
  proof_utils.test.ts
  status_checker.test.ts
  ```
- **Location:** Typically alongside the modules they test

**Example Test File:**
```typescript
// proof_utils.test.ts
import { validateProof } from './proof_utils';

describe('validateProof', () => {
  it('should return true for valid proof', () => {
    expect(validateProof(validData)).toBe(true);
  });
});
```

## Commands

| Command               | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| /generate-proof-batch | Generate a new batch of proof and status artifacts for documentation and release readiness |

```