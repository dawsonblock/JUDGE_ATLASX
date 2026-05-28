size-report:
	@find . -type f -not -path "./.git/*" -printf "%s %p\n" | sort -nr | head -30

PYTHON ?= python3
VERILATOR ?= verilator
RTL_SRCS := $(wildcard rtl/*.v)

.PHONY: all validate test lint audit-arith gen-lut cosim-vectors cosim-gkp extract-regs cdc-analyze parse-cdc cdc-gate-check lint-verilator clean-generated size-report cdc-signoff-package preboard-check implementation-gate vivado-signoff-package source-package proof-package validate-release release-validate release-proof-local

all:
	@echo "Available targets: validate, test, lint, audit-arith, gen-lut, cosim-vectors, cosim-gkp, extract-regs, cdc-analyze, parse-cdc, cdc-gate-check, lint-verilator, clean-generated, size-report, cdc-signoff-package, preboard-check, implementation-gate, vivado-signoff-package, source-package, proof-package, release-validate"

# Keep tests before generated heavy artifacts are recreated, otherwise compact-package
# tests correctly fail.
validate: clean-generated test lint gen-lut extract-regs cdc-analyze
	@echo "Validation completed. Note: this does not replace Vivado elaboration/timing."

test:
	PYTHONPATH=. $(PYTHON) -m unittest discover -s tests

lint:
	$(PYTHON) scripts/rtl_sanity_check.py

audit-arith:
	$(PYTHON) scripts/audit_rtl_arithmetic.py

gen-lut:
	$(PYTHON) scripts/generate_reciprocal_lut.py

extract-regs:
	$(PYTHON) scripts/extract_register_map.py

cdc-analyze: extract-regs
	$(PYTHON) scripts/analyze_cdc_crossings.py

lint-verilator:
	@if command -v $(VERILATOR) >/dev/null 2>&1; then \
		$(VERILATOR) --lint-only -Wall --timing $(RTL_SRCS); \
	else \
		echo "Verilator not installed; skipping lint-verilator"; \
	fi

parse-cdc:
	@if [ -f reports/cdc_critical.rpt ]; then \
		$(PYTHON) scripts/parse_cdc_report.py reports/cdc_critical.rpt --json-out reports/cdc_critical_summary.json; \
	else \
		echo "reports/cdc_critical.rpt not found; run Vivado report_cdc first."; \
	fi

cdc-gate-check:
	@if [ -f reports/cdc_full.rpt ]; then \
		$(PYTHON) scripts/parse_cdc_report.py reports/cdc_full.rpt --json-out reports/cdc_full_summary.json; \
	else \
		echo "reports/cdc_full.rpt not found; run Vivado report_cdc first."; \
	fi
	@if [ -f reports/cdc_critical.rpt ]; then \
		$(PYTHON) scripts/parse_cdc_report.py reports/cdc_critical.rpt --json-out reports/cdc_critical_summary.json --fail-on-critical; \
	else \
		echo "reports/cdc_critical.rpt not found; run Vivado report_cdc first."; \
	fi

cosim-vectors:
	$(PYTHON) scripts/generate_gkp_cosim_vectors.py --count 64

cosim-gkp:
	$(PYTHON) scripts/run_gkp_cosim.py

clean-generated:
	$(PYTHON) scripts/clean_generated_artifacts.py

cdc-signoff-package:
	$(PYTHON) scripts/package_cdc_signoff.py

preboard-check:
	$(PYTHON) scripts/preboard_check.py

implementation-gate:
	$(PYTHON) scripts/implementation_gate.py

vivado-signoff-package:
	$(PYTHON) scripts/package_vivado_signoff.py

source-package:
	$(PYTHON) scripts/build_release_archive.py --mode source

proof-package:
	$(PYTHON) scripts/build_release_archive.py --mode proof

validate-release:
	@latest_src=$$(ls -t dist/*-source-*.zip 2>/dev/null | head -1); \
	if [ -z "$$latest_src" ]; then \
		echo "No source archive found in dist/. Run make source-package first."; \
		exit 1; \
	fi; \
	$(PYTHON) scripts/validate_release_archive.py "$$latest_src" --mode source
	@latest_proof=$$(ls -t dist/*-proof-*.zip 2>/dev/null | head -1); \
	if [ -z "$$latest_proof" ]; then \
		echo "No proof archive found in dist/. Run make proof-package first."; \
		exit 1; \
	fi; \
	$(PYTHON) scripts/validate_release_archive.py "$$latest_proof" --mode proof

release-validate: preboard-check implementation-gate source-package proof-package validate-release
	@echo "release-validate complete"

release-proof-local: release-validate
	@echo "release-proof-local complete"
