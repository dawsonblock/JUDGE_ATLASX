.PHONY: backend-install backend-test frontend-install frontend-check frontend-typecheck verify docker-smoke proof backend-proof frontend-build bootstrap-backend bootstrap-frontend bootstrap truth-check full-proof clean-clone-proof release-proof-local release-package-proof-local nox test check-generated dev stop setup release-zip build-clean-release validate-release-zip proof-static

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
	@echo "=== Running authoritative proof bundle generation ==="
	@mkdir -p proof/latest
	@echo "=== 1. Runtime boundary checks ===" > proof/latest/proof_summary.log
	@python3 scripts/validate_runtime_boundaries.py > proof/latest/runtime_boundaries.log 2>&1 || (echo "FAIL: runtime boundaries" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: runtime boundaries" >> proof/latest/proof_summary.log
	@echo "=== 2. Frontend doctor ===" >> proof/latest/proof_summary.log
	@cd frontend && npm run doctor > ../proof/latest/frontend_doctor.log 2>&1 || (echo "FAIL: frontend doctor" >> ../proof/latest/proof_summary.log && exit 1)
	@echo "PASS: frontend doctor" >> proof/latest/proof_summary.log
	@echo "=== 3. Frontend build ===" >> proof/latest/proof_summary.log
	@cd frontend && npm run build > ../proof/latest/frontend_build.log 2>&1 || (echo "FAIL: frontend build" >> ../proof/latest/proof_summary.log && exit 1)
	@echo "PASS: frontend build" >> proof/latest/proof_summary.log
	@echo "=== 4. Source registry validation ===" >> proof/latest/proof_summary.log
	@python3 scripts/verify_source_registry.py > proof/latest/source_registry.log 2>&1 || (echo "FAIL: source registry" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: source registry" >> proof/latest/proof_summary.log
	@echo "=== 5. Evidence hash verification ===" >> proof/latest/proof_summary.log
	@python3 scripts/verify_snapshot_hashes.py > proof/latest/evidence_verify.log 2>&1 || (echo "FAIL: evidence hashes" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: evidence hashes" >> proof/latest/proof_summary.log
	@echo "=== 6. Audit chain verification ===" >> proof/latest/proof_summary.log
	@python3 scripts/verify_audit_chain.py > proof/latest/audit_chain.log 2>&1 || (echo "FAIL: audit chain" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: audit chain" >> proof/latest/proof_summary.log
	@echo "=== 7. Backend tests ===" >> proof/latest/proof_summary.log
	@cd backend && python -m pytest -q > ../proof/latest/backend_tests.log 2>&1 || (echo "FAIL: backend tests" >> ../proof/latest/proof_summary.log && exit 1)
	@echo "PASS: backend tests" >> proof/latest/proof_summary.log
	@echo "=== 8. Publication gate tests ===" >> proof/latest/proof_summary.log
	@cd backend && python -m pytest -q \
		app/tests/test_ingestion_result_gate.py \
		app/tests/test_machine_ingest_publication_block.py \
		app/tests/test_source_registry_contracts.py \
		app/tests/test_snapshot_integrity.py \
		app/tests/test_jwt_mutation_enforcement.py \
		app/tests/test_mutation_rbac_matrix.py \
		app/tests/test_review_gates.py \
		app/tests/test_evidence_required_for_publish.py \
		app/tests/test_ai_review_requires_reviewer_or_source_admin.py \
		app/tests/test_contradiction_intelligence.py \
		app/tests/test_claim_to_graph.py \
		app/tests/test_e2e_source_to_public_api.py \
		app/tests/test_public_api_safety.py > ../proof/latest/publication_gate.log 2>&1 || (echo "FAIL: publication gate tests" >> ../proof/latest/proof_summary.log && exit 1)
	@echo "PASS: publication gate tests" >> proof/latest/proof_summary.log
	@echo "=== 9. Contradiction tests ===" >> proof/latest/proof_summary.log
	@cd backend && python -m pytest -q app/tests/test_contradiction_intelligence.py > ../proof/latest/contradictions.log 2>&1 || (echo "FAIL: contradiction tests" >> ../proof/latest/proof_summary.log && exit 1)
	@echo "PASS: contradiction tests" >> proof/latest/proof_summary.log
	@echo "=== 10. Queue tests ===" >> proof/latest/proof_summary.log
	@cd backend && python -m pytest -q app/tests/test_postgres_queue.py > ../proof/latest/queue.log 2>&1 || (echo "FAIL: queue tests" >> ../proof/latest/proof_summary.log && exit 1)
	@echo "PASS: queue tests" >> proof/latest/proof_summary.log
	@echo "=== 11. OpenAPI contract tests ===" >> proof/latest/proof_summary.log
	@python3 scripts/check_api_contracts.py > proof/latest/openapi_contracts.log 2>&1 || (echo "FAIL: OpenAPI contracts" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: OpenAPI contracts" >> proof/latest/proof_summary.log
	@echo "=== 12. Release size check ===" >> proof/latest/proof_summary.log
	@python3 scripts/check_release_size.py > proof/latest/release_size.log 2>&1 || (echo "FAIL: release size" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: release size" >> proof/latest/proof_summary.log
	@echo "=== 13. Release gate ===" >> proof/latest/proof_summary.log
	@python3 scripts/release_gate.py > proof/latest/release_gate.log 2>&1 || (echo "FAIL: release gate" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: release gate" >> proof/latest/proof_summary.log
	@echo "=== 13.5. Proof artifact consistency check ===" >> proof/latest/proof_summary.log
	@cd backend && python -m app.ops.verify_proof_consistency > ../proof/latest/proof_consistency.log 2>&1 || (echo "FAIL: proof consistency" >> ../proof/latest/proof_summary.log && exit 1)
	@echo "PASS: proof consistency" >> proof/latest/proof_summary.log
	@echo "=== 14. Proof timestamp staleness check ===" >> proof/latest/proof_summary.log
	@python3 scripts/check_proof_timestamp.py > proof/latest/timestamp.log 2>&1 || (echo "FAIL: proof timestamp" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: proof timestamp" >> proof/latest/proof_summary.log
	@echo "=== 15. Generate proof artifacts ===" >> proof/latest/proof_summary.log
	@python3 scripts/generate_alpha_proof_artifacts.py > proof/latest/generate_artifacts.log 2>&1 || (echo "FAIL: generate artifacts" >> proof/latest/proof_summary.log && exit 1)
	@echo "PASS: generate artifacts" >> proof/latest/proof_summary.log
	@cp artifacts/current/PROOF_REPORT.md proof/latest/
	@cp artifacts/current/PROOF_MANIFEST.json proof/latest/
	@cp artifacts/current/RELEASE_MANIFEST.json proof/latest/
	@echo "=== Proof complete: proof/latest/ ===" >> proof/latest/proof_summary.log
	@echo "Files: PROOF_REPORT.md, PROOF_MANIFEST.json, RELEASE_MANIFEST.json" >> proof/latest/proof_summary.log
	@echo "=== Proof complete: proof/latest/ ==="
	@echo "Files: PROOF_REPORT.md, PROOF_MANIFEST.json, RELEASE_MANIFEST.json"

build-clean-release:
	@python3 scripts/build_clean_release.py

validate-release-zip:
	@python3 scripts/validate_release_zip.py

# proof-static: dependency-free boundary checks (no backend install required)
proof-static:
	@python3 scripts/validate_runtime_boundaries.py --static-only
	@python3 scripts/check_truth_claims.py --root .
	@echo "Static boundary checks complete (no backend install required)"

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
