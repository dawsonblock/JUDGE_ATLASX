# Source Coverage Matrix

Generated: 2026-05-16T21:07:58.908807+00:00

| source key | jurisdiction | class | adapter status | proof status | public default | next action |
|---|---|---|---|---|---|---|
| justice_canada_laws_xml | Canada | machine_ingest | found | configured | false | None. Source is pinned and enabled. Monitor ingestion runs and review queue for new snapshots. |
| justice_canada_laws_pit_xml | Canada | disabled_stub | missing_parser | configured | false | Write a PIT-date-parameterised adapter or remove if not needed. |
| scc_judgments | Canada | machine_ingest | found | configured | false | Migrate any references from scc_judgments to scc_decisions and remove this entry. |
| federal_court_canada_decisions | Canada | portal_reference | found | configured | false | Migrate any references from federal_court_canada_decisions to federal_court_canada and remove this entry. |
| statscan_crime_tables | Canada | portal_reference | found | configured | false | Monitor StatsCan API roadmap; build adapter if open data endpoint is published. |
| saskatchewan_legislation | CA-SK | portal_reference | missing_parser | configured | false | Evaluate whether an RSS/XML feed can be configured; otherwise keep as portal_reference. |
| saskatoon_open_data_public_safety | CA-SK-Saskatoon | portal_reference | found | configured | false | Check data.saskatoon.ca for CSV/JSON endpoint; write adapter if machine-readable. |
| saskatoon_open_data_crime | Saskatoon, Saskatchewan, Canada | portal_reference | found | configured | false | Check data.saskatoon.ca for updated CSV/JSON endpoint; write adapter if machine-readable. |
| saskatoon_police_open_data | Saskatoon, Saskatchewan, Canada | portal_reference | found | configured | false | Monitor Saskatoon Police data portal for a machine-readable feed. |
| web_monitor_saskatoon_police_news | Saskatoon, Saskatchewan, Canada | disabled_stub | found | configured | false | Evaluate whether a scraper is required or remove this stub. |
| sk_courts_qb_decisions | Saskatchewan, Canada | machine_ingest | found | configured | false | Confirm terms of use, then /enable via admin panel. |
| sk_courts_ca_decisions | Saskatchewan, Canada | machine_ingest | found | configured | false | Confirm terms of use, then /enable via admin panel. |
| statscan_ccjs_crime_sk | Saskatchewan, Canada | portal_reference | found | configured | false | Monitor StatsCan open data API for a machine-readable CCJS endpoint. |
| statscan_ucr_national | Canada | portal_reference | found | configured | false | Monitor StatsCan open data API for a machine-readable UCR endpoint. |
| canlii_sk | Saskatchewan, Canada | portal_reference | found | configured | false | Negotiate data access agreement with CanLII, or use only as a reference link. |
| federal_court_canada | Canada | machine_ingest | found | configured | false | Confirm base_url is reachable and terms permit ingest, then /enable via admin panel. |
| scc_decisions | Canada | machine_ingest | found | configured | false | Confirm base_url is reachable and terms permit ingest, then /enable via admin panel. |
| sk_justice_ministry | Saskatchewan, Canada | disabled_stub | found | configured | false | Define what specific data is needed, then write a targeted adapter. |
| sk_legislature_hansard | Saskatchewan, Canada | machine_ingest | found | configured | false | Confirm base_url is reachable and terms permit ingest, then /enable via admin panel. |
| canada_open_data_crime | Canada | portal_reference | found | configured | false | Validate open.canada.ca API endpoint and write adapter. |
| rcmp_sk_news | Saskatchewan, Canada | disabled_stub | found | configured | false | Evaluate whether a scraper is required or remove this stub. |
| canada_justice_laws | Canada | disabled_stub | missing_parser | configured | false | Remove all references to canada_justice_laws and use justice_canada_laws_xml instead. |
| saskatoon_open_data_portal | Saskatoon, Saskatchewan, Canada | portal_reference | found | configured | false | Prefer specific source_key entries per dataset. |
| justice_canada_laws_xml_repo | Canada | manual_reference | missing_parser | configured | false | Use justice_canada_laws_xml as the live ingest source. This entry is for schema and DTD reference only. |
| justice_canada_lims_xml_dtd | Canada | manual_reference | missing_parser | configured | false | Keep as a documentation reference; not a data source. |
| justice_canada_otto_reference | Canada | manual_reference | missing_parser | configured | false | Keep as a documentation reference; not a data source. |

Notes:
- Public default is intentionally conservative in alpha and does not bypass review/evidence gates.
- Evidence is authoritative; AI and memory outputs are derivative only.
