# SOURCE_REGISTRY_STATUS

- generated_at_utc: 2026-05-15T04:43:28.908943+00:00
- commit_hash: 16d6b61c15cc3785033a4c0435f2da1f81eb4e0d
- total_sources: 26
- machine_ingest_sources: 7
- runnable_when_active_sources: unknown
- enableable_sources: unknown
- sources_requiring_secrets: unknown

| source key | source name | jurisdiction | source class/type | automation status | adapter key | adapter exists | required secrets | required secrets present during proof | enabled by default | can be enabled by admin | can run now | reason if not runnable | review required before public visibility | public exposure allowed before review | current alpha status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| canada_justice_laws |  | Canada | disabled_stub/aggregate_stats | disabled_stub | None | no | none | no | no | no | no | none | yes | no | limited-alpha-source |
| canada_open_data_crime |  | Canada | portal_reference/aggregate_stats | adapter_missing | ckan_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| canlii_sk |  | Saskatchewan, Canada | portal_reference/court_record | adapter_missing | canlii_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| federal_court_canada |  | Canada | machine_ingest/court_record | machine_ready_disabled | federal_court_html | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| federal_court_canada_decisions |  | Canada | portal_reference/court_record | adapter_missing | federal_court_html | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| justice_canada_laws_pit_xml |  | Canada | disabled_stub/legislation | adapter_missing | None | no | none | no | no | no | no | none | yes | no | limited-alpha-source |
| justice_canada_laws_xml |  | Canada | machine_ingest/legislation | machine_ready_enabled | laws_justice_xml | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| justice_canada_laws_xml_repo |  | Canada | manual_reference/reference_repository | adapter_missing | None | no | none | no | no | no | no | none | yes | no | limited-alpha-source |
| justice_canada_lims_xml_dtd |  | Canada | manual_reference/schema_reference | adapter_missing | None | no | none | no | no | no | no | none | yes | no | limited-alpha-source |
| justice_canada_otto_reference |  | Canada | manual_reference/architecture_reference | adapter_missing | None | no | none | no | no | no | no | none | yes | no | limited-alpha-source |
| rcmp_sk_news |  | Saskatchewan, Canada | disabled_stub/news_monitor | adapter_missing | crawlee_police_release | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| saskatchewan_legislation |  | CA-SK | portal_reference/legislation | adapter_missing | None | no | none | no | no | no | no | none | yes | no | limited-alpha-source |
| saskatoon_open_data_crime |  | Saskatoon, Saskatchewan, Canada | portal_reference/crime_incident | adapter_missing | saskatoon_csv | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| saskatoon_open_data_portal |  | Saskatoon, Saskatchewan, Canada | portal_reference/aggregate_stats | adapter_missing | ckan_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| saskatoon_open_data_public_safety |  | CA-SK-Saskatoon | portal_reference/aggregate_stats | adapter_missing | ckan_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| saskatoon_police_open_data |  | Saskatoon, Saskatchewan, Canada | portal_reference/crime_incident | adapter_missing | saskatoon_police_csv | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| scc_decisions |  | Canada | machine_ingest/court_record | machine_ready_disabled | scc_lexum_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| scc_judgments |  | Canada | machine_ingest/court_record | machine_ready_disabled | scc_lexum_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| sk_courts_ca_decisions |  | Saskatchewan, Canada | machine_ingest/court_record | machine_ready_disabled | canlii_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| sk_courts_qb_decisions |  | Saskatchewan, Canada | machine_ingest/court_record | machine_ready_disabled | canlii_api | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| sk_justice_ministry |  | Saskatchewan, Canada | disabled_stub/news_monitor | adapter_missing | crawlee_gov_news | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| sk_legislature_hansard |  | Saskatchewan, Canada | machine_ingest/aggregate_stats | machine_ready_disabled | sk_legislature_html | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| statscan_ccjs_crime_sk |  | Saskatchewan, Canada | portal_reference/aggregate_stats | adapter_missing | statscan_table | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| statscan_crime_tables |  | Canada | portal_reference/aggregate_stats | adapter_missing | statscan_table | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| statscan_ucr_national |  | Canada | portal_reference/aggregate_stats | adapter_missing | statscan_table | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |
| web_monitor_saskatoon_police_news |  | Saskatoon, Saskatchewan, Canada | disabled_stub/news_monitor | adapter_missing | crawlee_police_release | yes | none | no | no | no | no | none | yes | no | limited-alpha-source |

- artifacts/proof/current/source_registry_status.json
