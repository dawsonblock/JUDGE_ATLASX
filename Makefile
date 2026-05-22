.PHONY: backend-install backend-test frontend-install frontend-check frontend-typecheck verify docker-smoke proof backend-proof frontend-build bootstrap-backend bootstrap-frontend bootstrap truth-check full-proof clean-clone-proof release-proof-local release-package-proof-local nox test check-generated dev stop setup release-zip build-clean-release validate-release-zip proof-static validate-archive-freshness saskatoon-staging-proof canlii-staging-contract statscan-boundary-proof validate-smoke-workspace validate-full-workspace validate-docker-workspace

backend-install:
	cd backend && python -m pip install -e ".[test]"

backend-test:
	cd backend && python -m compileall -q app
	cd backend && python -m pytest -q

frontend-install:
	cd frontend && npm ci

frontend-check:
	cd frontend && npm run lint
	cd frontend && npm run typecheck
	cd frontend && npm run build

frontend-build:
	cd frontend && npm run build

frontend-typecheck:
	cd frontend && npm run typecheck

bootstrap-backend:
	bash scripts/bootstrap_backend.sh

bootstrap-frontend:
	bash scripts/bootstrap_frontend.sh

bootstrap:
	bash scripts/bootstrap_all.sh

# ---------------------------------------------------------------------------
# Local development
# ---------------------------------------------------------------------------

# setup: copy .env.example → .env (if not present) then install all deps
setup:
	@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env from .env.example — review tokens before production use"; fi
	bash scripts/bootstrap_all.sh

# dev: start the full stack via Docker Compose (creates .env automatically)
dev:
	@if [ ! -f .env ]; then cp .env.example .env && echo "Created .env from .env.example — review tokens before production use"; fi
	docker compose up --build

# stop: tear down Docker Compose services
stop:
	docker compose down

truth-check:
	python3 scripts/check_truth_claims.py --root .
	python3 scripts/validate_workflows.py
	python3 scripts/check_source_keys.py
	python3 scripts/check_statuses.py

check-generated:
	python3 scripts/check_no_generated_files.py --root .

nox:
	nox

full-proof:
	bash scripts/proof_full_stack.sh

release-proof-local:
	@if [ -x backend/.venv/bin/python ]; then \
		backend/.venv/bin/python scripts/release_gate.py; \
	else \
		python3 scripts/release_gate.py; \
	fi

release-package-proof-local:
	bash scripts/package_and_validate_release_archive.sh

clean-clone-proof:
	bash scripts/proof_clean_clone.sh

backend-proof:
	cd backend && python scripts/proof_backend_import.py

# test is an alias for backend-test
test: backend-test

# verify runs the full quality gate (no Docker)
verify: check-generated truth-check backend-install backend-test frontend-install frontend-check

docker-smoke:
	docker compose up -d --build
	curl -f http://localhost:8000/docs >/dev/null
	curl -f http://localhost:3000 >/dev/null
	docker compose down -v

proof:
	@echo "=== Running canonical proof generation ==="
	@$(MAKE) release-proof-local
	@python3 scripts/check_single_proof_authority.py
	@python3 scripts/check_proof_consistency.py
	@python3 scripts/check_proof_freshness.py
	@python3 scripts/check_required_proof_logs.py
	@echo "Canonical proof: artifacts/proof/current/release_gate.json"

validate-archive-freshness:
	@python3 scripts/verify_archive_proof_freshness.py --archive $(ARCHIVE)

saskatoon-staging-proof:
	@backend/.venv/bin/python -m pytest backend/app/tests/test_saskatoon_open_data_staging.py -q

canlii-staging-contract:
	@backend/.venv/bin/python -m pytest backend/app/tests/test_saskatchewan_court_sources.py backend/app/tests/test_canlii_sk_ingest.py -q

statscan-boundary-proof:
	@backend/.venv/bin/python -m pytest backend/app/tests/test_statscan_table_adapter_boundary.py backend/app/tests/test_source_registry_consistency.py -q

build-clean-release:
	@echo "DEPRECATED: use make release-package-proof-local (authoritative pipeline)"
	@bash scripts/package_and_validate_release_archive.sh --archive-path dist/JUDGE_ATLAS-main-final.zip --package-root-name JUDGE_ATLAS-main

validate-release-zip:
	@echo "DEPRECATED: use validate_final_zip/check_release_surface/verify_archive_proof_freshness on dist/JUDGE_ATLAS-main-final.zip"
	@python3 scripts/validate_final_zip.py dist/JUDGE_ATLAS-main-final.zip
	@python3 scripts/check_release_surface.py --archive dist/JUDGE_ATLAS-main-final.zip
	@python3 scripts/verify_archive_proof_freshness.py --archive dist/JUDGE_ATLAS-main-final.zip

validate-smoke-workspace:
	@TOOLATHLON_PROFILE=smoke bash scripts/validate_smoke_workspace.sh

validate-full-workspace:
	@TOOLATHLON_PROFILE=full bash scripts/validate_full_workspace.sh

validate-docker-workspace:
	@TOOLATHLON_PROFILE=smoke RUN_DOCKER=1 bash scripts/validate_smoke_workspace.sh

# proof-static: dependency-free boundary checks (no backend install required)
proof-static:
	@python3 scripts/validate_runtime_boundaries.py --static-only
	@python3 scripts/check_truth_claims.py --root .
	@echo "Static boundary checks complete (no backend install required)"

# release-zip: create a distributable archive excluding development artifacts
release-zip:
	@VERSION=$$(date +%Y%m%d-%H%M%S); \
	OUTFILE="judge_atlas_$${VERSION}.zip"; \
	bash scripts/create_release_zip.sh --output "$${OUTFILE}"; \
	echo "Release archive: $${OUTFILE}"
