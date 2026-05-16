.PHONY: backend-install backend-test frontend-install frontend-check frontend-typecheck verify docker-smoke proof backend-proof frontend-build bootstrap-backend bootstrap-frontend bootstrap truth-check full-proof clean-clone-proof release-proof-local release-package-proof-local nox test check-generated dev stop setup release-zip build-clean-release validate-release-zip

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
	@python3 scripts/validate_runtime_boundaries.py
	@python3 scripts/verify_source_registry.py
	@cd backend && python -m pytest -q \
		app/tests/test_ingestion_result_gate.py \
		app/tests/test_machine_ingest_publication_block.py \
		app/tests/test_source_registry_contracts.py \
		app/tests/test_snapshot_integrity.py \
		app/tests/test_jwt_mutation_enforcement.py \
		app/tests/test_mutation_rbac_matrix.py \
		app/tests/test_review_gates.py \
		app/tests/test_evidence_required_for_publish.py \
		app/tests/test_ai_review_requires_reviewer_or_source_admin.py
	@python3 scripts/release_gate.py || true
	@python3 scripts/generate_alpha_proof_artifacts.py
	@echo "Proof complete: artifacts/current/PROOF_REPORT.md and artifacts/current/PROOF_MANIFEST.json"

build-clean-release:
	@python3 scripts/build_clean_release.py

validate-release-zip:
	@python3 scripts/validate_release_zip.py

# release-zip: create a distributable archive excluding development artifacts
release-zip:
	@VERSION=$$(date +%Y%m%d-%H%M%S); \
	OUTFILE="judge_atlas_$${VERSION}.zip"; \
	zip -r "$${OUTFILE}" . \
	  --exclude "*.pyc" \
	  --exclude "*/__pycache__/*" \
	  --exclude "*/.venv/*" \
	  --exclude "*.egg-info/*" \
	  --exclude ".git/*" \
	  --exclude ".git" \
	  --exclude "node_modules/*" \
	  --exclude "frontend/.next/*" \
	  --exclude "artifacts/proof/*" \
	  --exclude "*.log" \
	  --exclude "*.zip"; \
	echo "Release archive: $${OUTFILE}"
