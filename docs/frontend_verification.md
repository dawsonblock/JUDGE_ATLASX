# Frontend Verification Guide

## Node Version Requirement

The frontend requires **Node 24**. This is enforced at three levels:

| Location | Setting |
|---|---|
| `frontend/.nvmrc` | `24` |
| `frontend/package.json` engines | `>=24.0.0` |
| `scripts/release_gate.py` | `nvm use 24` + `--expected-major 24` |
| `scripts/check_frontend_node_gate.py` | defaults `--expected-major 24 --expected-minor 0` |

## Setup

```bash
# Install and activate Node 24 via nvm
nvm install 24
nvm use 24

# Verify
node --version   # must be v24.x.x

# Install dependencies
cd frontend
npm ci

# Run checks
npm run lint
npm run typecheck
npm run test:contracts
npm run build
```

## Automatic Version Switching

With `frontend/.nvmrc` present, `nvm` will automatically switch to Node 24 when you `cd frontend` if you have `nvm` shell hooks enabled.

## Common Failure Modes

### `BLOCKED_NODE_VERSION`
The release gate emits this signal when `nvm use 24` fails. Fix:
```bash
nvm install 24
nvm use 24
```

### `engine-strict` rejection
`frontend/.npmrc` sets `engine-strict=true`. If you run `npm install` or `npm ci`
under the wrong Node version, npm will reject with an engines violation. Fix:
switch to Node 24 first, then retry.

### `vitest: command not found`
Occurs when `npm ci` was not run. Run `npm ci` under Node 24 before running tests.

## CI Reference

The release gate (`scripts/release_gate.py`) runs all frontend steps under
`nvm use 24` and validates the version with `scripts/check_frontend_node_gate.py`.

A mismatch between the running Node version and Node 24 causes the
`frontend_node_gate` step to emit `BLOCKED_NODE_VERSION` and fail with exit 1.
The gate does not fall back to other Node versions.
