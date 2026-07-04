# SingleLineIQ Engineering Review Report

> This report was generated from synthetic anonymized data for demonstration purposes only. It is not based on a real plant, project, client, or confidential engineering deliverable.

## Executive Summary

- Electrical assets: **23**
- Final loads: **121**
- Total connected load: **6718.1 kW**
- Deterministic issues: **16**
- SLD cross-check issues: **111**

## Top Loaded Assets

| Asset | Type | Capacity kW | Downstream Load kW | Utilization % |
|---|---:|---:|---:|---:|
| KPL2-GRID-3300-UTIL01 | UG | 10000.0 | 6699.6 | 67.0 |
| KPL2-MAIN-3300-SWGR01 | HV | 8000.0 | 6699.6 | 83.7 |
| KPL2-MAIN-3300-TR00 | TA | 6300.0 | 6699.6 | 106.3 |
| KPL2-MAIN-6600-MVDB01 | HV | 6000.0 | 6699.6 | 111.7 |
| KPL2-C30-430-MV01-SWBD03 | HV | 4000.0 | 3360.0 | 84.0 |
| KPL2-C30-430-MV01-SWG01 | HV | 3800.0 | 3360.0 | 88.4 |
| KPL2-B20-420-TR02 | TA | 1600.0 | 1634.2 | 102.1 |
| KPL2-B20-420-LV02-SWBD02 | LV | 1500.0 | 1634.2 | 109.0 |
| KPL2-B20-420-LV02-MCC03 | MCC | 900.0 | 1141.0 | 126.8 |
| KPL2-A10-410-TR01 | TA | 1250.0 | 1126.7 | 90.1 |
| KPL2-A10-410-LV01-SWBD01 | LV | 1200.0 | 1126.7 | 93.9 |
| KPL2-C30-430-TR03 | TA | 1500.0 | 578.7 | 38.6 |
| KPL2-C30-430-LV03-SWBD03 | LV | 900.0 | 578.7 | 64.3 |
| KPL2-A10-410-LV01-MCC01 | MCC | 520.0 | 434.8 | 83.6 |
| KPL2-C30-430-LV03-MCC05 | MCC | 500.0 | 430.5 | 86.1 |

## Deterministic Findings

### DET-001 — Duplicate ITEM TAG detected: KPL2-B20-420-MX099
- Severity: **high**
- Type: `DUPLICATE_ITEM_TAG`
- Item: `KPL2-B20-420-MX099`
- Evidence: `{'count': 2}`
- Recommendation: Keep a unique ITEM TAG per asset/load or confirm intentional duplicate handling.

### DET-002 — Parent item tag not found for KPL2-Z90-999-TR99
- Severity: **critical**
- Type: `PARENT_NOT_FOUND`
- Item: `KPL2-Z90-999-TR99`
- Evidence: `{'missing_parent': 'KPL2-UNKNOWN-FEEDER'}`
- Recommendation: Correct the parent hierarchy or add the missing upstream asset row.

### DET-003 — Final load has missing RATED POWER: KPL2-C30-430-FN001
- Severity: **medium**
- Type: `MISSING_RATED_POWER`
- Item: `KPL2-C30-430-FN001`
- Evidence: `{'item_tag': 'KPL2-C30-430-FN001', 'rated_power': None}`
- Recommendation: Populate RATED POWER before final load aggregation or capacity review.

### DET-004 — KPL2-MAIN-3300-TR00 exceeds capacity
- Severity: **critical**
- Type: `ASSET_OVERLOAD`
- Item: `KPL2-MAIN-3300-TR00`
- Evidence: `{'capacity_kw': 6300.0, 'downstream_load_kw': 6699.6, 'utilization_percent': 106.34}`
- Recommendation: Review load allocation, capacity rating, or design criteria.

### DET-005 — KPL2-MAIN-6600-MVDB01 exceeds capacity
- Severity: **critical**
- Type: `ASSET_OVERLOAD`
- Item: `KPL2-MAIN-6600-MVDB01`
- Evidence: `{'capacity_kw': 6000.0, 'downstream_load_kw': 6699.6, 'utilization_percent': 111.66}`
- Recommendation: Review load allocation, capacity rating, or design criteria.

### DET-006 — KPL2-A10-410-TR01 is highly loaded
- Severity: **medium**
- Type: `HIGH_ASSET_LOADING`
- Item: `KPL2-A10-410-TR01`
- Evidence: `{'capacity_kw': 1250.0, 'downstream_load_kw': 1126.7, 'utilization_percent': 90.14}`
- Recommendation: Verify spare capacity and future load allowance.

### DET-007 — KPL2-B20-420-TR02 exceeds capacity
- Severity: **critical**
- Type: `ASSET_OVERLOAD`
- Item: `KPL2-B20-420-TR02`
- Evidence: `{'capacity_kw': 1600.0, 'downstream_load_kw': 1634.2, 'utilization_percent': 102.14}`
- Recommendation: Review load allocation, capacity rating, or design criteria.

### DET-008 — KPL2-A10-410-LV01-SWBD01 is highly loaded
- Severity: **medium**
- Type: `HIGH_ASSET_LOADING`
- Item: `KPL2-A10-410-LV01-SWBD01`
- Evidence: `{'capacity_kw': 1200.0, 'downstream_load_kw': 1126.7, 'utilization_percent': 93.89}`
- Recommendation: Verify spare capacity and future load allowance.

### DET-009 — KPL2-B20-420-LV02-SWBD02 exceeds capacity
- Severity: **critical**
- Type: `ASSET_OVERLOAD`
- Item: `KPL2-B20-420-LV02-SWBD02`
- Evidence: `{'capacity_kw': 1500.0, 'downstream_load_kw': 1634.2, 'utilization_percent': 108.95}`
- Recommendation: Review load allocation, capacity rating, or design criteria.

### DET-010 — High VSD concentration on KPL2-A10-410-LV01-MCC01
- Severity: **medium**
- Type: `HIGH_VSD_CONCENTRATION`
- Item: `KPL2-A10-410-LV01-MCC01`
- Evidence: `{'vsd_percent': 72.73, 'vsd_count': 16, 'load_count': 22}`
- Recommendation: Review harmonic/filtering assumptions and VSD grouping.

### DET-011 — KPL2-A10-410-LV01-MCC02 is highly loaded
- Severity: **medium**
- Type: `HIGH_ASSET_LOADING`
- Item: `KPL2-A10-410-LV01-MCC02`
- Evidence: `{'capacity_kw': 450.0, 'downstream_load_kw': 399.4, 'utilization_percent': 88.76}`
- Recommendation: Verify spare capacity and future load allowance.

### DET-012 — KPL2-B20-420-LV02-MCC03 exceeds capacity
- Severity: **critical**
- Type: `ASSET_OVERLOAD`
- Item: `KPL2-B20-420-LV02-MCC03`
- Evidence: `{'capacity_kw': 900.0, 'downstream_load_kw': 1141.0, 'utilization_percent': 126.78}`
- Recommendation: Review load allocation, capacity rating, or design criteria.

### DET-013 — High VSD concentration on KPL2-B20-420-LV02-MCC03
- Severity: **medium**
- Type: `HIGH_VSD_CONCENTRATION`
- Item: `KPL2-B20-420-LV02-MCC03`
- Evidence: `{'vsd_percent': 83.33, 'vsd_count': 15, 'load_count': 18}`
- Recommendation: Review harmonic/filtering assumptions and VSD grouping.

### DET-014 — KPL2-B20-420-LV02-MCC04 is highly loaded
- Severity: **medium**
- Type: `HIGH_ASSET_LOADING`
- Item: `KPL2-B20-420-LV02-MCC04`
- Evidence: `{'capacity_kw': 450.0, 'downstream_load_kw': 384.2, 'utilization_percent': 85.38}`
- Recommendation: Verify spare capacity and future load allowance.

### DET-015 — KPL2-C30-430-LV03-MCC05 is highly loaded
- Severity: **medium**
- Type: `HIGH_ASSET_LOADING`
- Item: `KPL2-C30-430-LV03-MCC05`
- Evidence: `{'capacity_kw': 500.0, 'downstream_load_kw': 430.5, 'utilization_percent': 86.1}`
- Recommendation: Verify spare capacity and future load allowance.

### DET-016 — KPL2-C30-430-MV01-SWG01 is highly loaded
- Severity: **medium**
- Type: `HIGH_ASSET_LOADING`
- Item: `KPL2-C30-430-MV01-SWG01`
- Evidence: `{'capacity_kw': 3800.0, 'downstream_load_kw': 3360.0, 'utilization_percent': 88.42}`
- Recommendation: Verify spare capacity and future load allowance.

## SLD Visual Cross-Check Findings

### SLD-001 — Consumer-list asset not visible in SLD: KPL2-C30-430-LV03-MCC06
- Severity: **high**
- Confidence: **1.00**
- Item: `KPL2-C30-430-LV03-MCC06`
- Evidence: `{'consumer_parent': 'KPL2-C30-430-LV03-SWBD03', 'equipment_type': 'MCC'}`
- Recommendation: Verify whether this asset is missing from the single-line diagram or uses a different tag.

### SLD-002 — SLD-only asset not found in consumer list: KPL2-A10-410-PP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-003 — SLD-only asset not found in consumer list: KPL2-A10-410-FN001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-004 — SLD-only asset not found in consumer list: KPL2-A10-410-FN002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-005 — SLD-only asset not found in consumer list: KPL2-A10-410-CP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-006 — SLD-only asset not found in consumer list: KPL2-A10-410-MX001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-007 — SLD-only asset not found in consumer list: KPL2-A10-410-MX002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-008 — SLD-only asset not found in consumer list: KPL2-A10-410-PP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-009 — SLD-only asset not found in consumer list: KPL2-A10-410-MX003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX003`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-010 — SLD-only asset not found in consumer list: KPL2-A10-410-MX004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX004`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-011 — SLD-only asset not found in consumer list: KPL2-A10-410-MX005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX005`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-012 — SLD-only asset not found in consumer list: KPL2-A10-410-PP003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP003`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-013 — SLD-only asset not found in consumer list: KPL2-A10-410-CP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-014 — SLD-only asset not found in consumer list: KPL2-A10-410-PP004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP004`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-015 — SLD-only asset not found in consumer list: KPL2-A10-410-FN003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN003`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-016 — SLD-only asset not found in consumer list: KPL2-A10-410-CP003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP003`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-017 — SLD-only asset not found in consumer list: KPL2-A10-410-FN004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN004`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-018 — SLD-only asset not found in consumer list: KPL2-A10-410-CP004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP004`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-019 — SLD-only asset not found in consumer list: KPL2-A10-410-CP005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP005`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-020 — SLD-only asset not found in consumer list: KPL2-A10-410-FN005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN005`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-021 — SLD-only asset not found in consumer list: KPL2-A10-410-MX006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX006`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-022 — SLD-only asset not found in consumer list: KPL2-A10-410-MX007
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX007`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-023 — SLD-only asset not found in consumer list: KPL2-A10-410-FN006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN006`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-024 — SLD-only asset not found in consumer list: KPL2-A10-410-PK001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PK001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-025 — SLD-only asset not found in consumer list: KPL2-A10-410-FN007
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN007`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-026 — SLD-only asset not found in consumer list: KPL2-A10-410-PP005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP005`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-027 — SLD-only asset not found in consumer list: KPL2-A10-410-FN008
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN008`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-028 — SLD-only asset not found in consumer list: KPL2-A10-410-CP006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP006`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-029 — SLD-only asset not found in consumer list: KPL2-A10-410-HT001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-HT001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-030 — SLD-only asset not found in consumer list: KPL2-A10-410-PP006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP006`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-031 — SLD-only asset not found in consumer list: KPL2-A10-410-CP007
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP007`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-032 — SLD-only asset not found in consumer list: KPL2-A10-410-MX008
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-MX008`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-033 — SLD-only asset not found in consumer list: KPL2-A10-410-HT002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-HT002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-034 — SLD-only asset not found in consumer list: KPL2-A10-410-HT003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-HT003`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-035 — SLD-only asset not found in consumer list: KPL2-A10-410-CP008
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-CP008`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-036 — SLD-only asset not found in consumer list: KPL2-A10-410-PK002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PK002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-037 — SLD-only asset not found in consumer list: KPL2-A10-410-PP007
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP007`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-038 — SLD-only asset not found in consumer list: KPL2-A10-410-PP008
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP008`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-039 — SLD-only asset not found in consumer list: KPL2-A10-410-FN009
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-FN009`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-MCC02', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-040 — SLD-only asset not found in consumer list: KPL2-A10-410-HT004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-HT004`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-041 — SLD-only asset not found in consumer list: KPL2-A10-410-PK003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PK003`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-042 — SLD-only asset not found in consumer list: KPL2-A10-410-LP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-LP001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'AL'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-043 — SLD-only asset not found in consumer list: KPL2-A10-410-UP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-UP001`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'USPB'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-044 — SLD-only asset not found in consumer list: KPL2-A10-410-UP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-UP002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'USPB'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-045 — SLD-only asset not found in consumer list: KPL2-A10-410-LP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-LP002`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'AL'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-046 — SLD-only asset not found in consumer list: KPL2-A10-410-HT005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-HT005`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-047 — SLD-only asset not found in consumer list: KPL2-A10-410-HT006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-HT006`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-048 — SLD-only asset not found in consumer list: KPL2-B20-420-PP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PP001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-049 — SLD-only asset not found in consumer list: KPL2-B20-420-MX001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-MX001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-050 — SLD-only asset not found in consumer list: KPL2-B20-420-PP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PP002`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-051 — SLD-only asset not found in consumer list: KPL2-B20-420-MX099
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-MX099`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-052 — SLD-only asset not found in consumer list: KPL2-B20-420-CP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-053 — SLD-only asset not found in consumer list: KPL2-B20-420-CP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP002`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-054 — SLD-only asset not found in consumer list: KPL2-B20-420-PK001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-055 — SLD-only asset not found in consumer list: KPL2-B20-420-PP003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PP003`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-056 — SLD-only asset not found in consumer list: KPL2-B20-420-CP003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP003`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-057 — SLD-only asset not found in consumer list: KPL2-B20-420-CP004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP004`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-058 — SLD-only asset not found in consumer list: KPL2-B20-420-PP004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PP004`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-059 — SLD-only asset not found in consumer list: KPL2-B20-420-MX004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-MX004`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-060 — SLD-only asset not found in consumer list: KPL2-B20-420-PK002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK002`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-061 — SLD-only asset not found in consumer list: KPL2-B20-420-PK003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK003`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-062 — SLD-only asset not found in consumer list: KPL2-B20-420-PP005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PP005`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-063 — SLD-only asset not found in consumer list: KPL2-B20-420-PP006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PP006`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-064 — SLD-only asset not found in consumer list: KPL2-B20-420-PP007
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PP007`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC03', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-065 — SLD-only asset not found in consumer list: KPL2-B20-420-CP005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP005`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-066 — SLD-only asset not found in consumer list: KPL2-B20-420-MX005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-MX005`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-067 — SLD-only asset not found in consumer list: KPL2-B20-420-HT001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-HT001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-068 — SLD-only asset not found in consumer list: KPL2-B20-420-PK004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK004`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-069 — SLD-only asset not found in consumer list: KPL2-B20-420-CP006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP006`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-070 — SLD-only asset not found in consumer list: KPL2-B20-420-CP007
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP007`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-071 — SLD-only asset not found in consumer list: KPL2-B20-420-MX006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-MX006`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-072 — SLD-only asset not found in consumer list: KPL2-B20-420-FN001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-FN001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-073 — SLD-only asset not found in consumer list: KPL2-B20-420-HT002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-HT002`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-074 — SLD-only asset not found in consumer list: KPL2-B20-420-HT003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-HT003`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-075 — SLD-only asset not found in consumer list: KPL2-B20-420-CP008
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP008`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-076 — SLD-only asset not found in consumer list: KPL2-B20-420-HT004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-HT004`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-077 — SLD-only asset not found in consumer list: KPL2-B20-420-CP009
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-CP009`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-078 — SLD-only asset not found in consumer list: KPL2-B20-420-HT005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-HT005`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-MCC04', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-079 — SLD-only asset not found in consumer list: KPL2-B20-420-UP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-UP001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'USPB'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-080 — SLD-only asset not found in consumer list: KPL2-B20-420-LP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-LP001`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'AL'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-081 — SLD-only asset not found in consumer list: KPL2-B20-420-LP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-LP002`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'AL'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-082 — SLD-only asset not found in consumer list: KPL2-B20-420-PK005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK005`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-083 — SLD-only asset not found in consumer list: KPL2-B20-420-PK006
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK006`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-084 — SLD-only asset not found in consumer list: KPL2-B20-420-UP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-UP002`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'USPB'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-085 — SLD-only asset not found in consumer list: KPL2-B20-420-PK007
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK007`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-086 — SLD-only asset not found in consumer list: KPL2-B20-420-PK008
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK008`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-087 — SLD-only asset not found in consumer list: KPL2-B20-420-PK009
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-B20-420-PK009`
- Evidence: `{'visual_parent': 'KPL2-B20-420-LV02-DB02', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-088 — SLD-only asset not found in consumer list: KPL2-C30-430-MX001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-MX001`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-089 — SLD-only asset not found in consumer list: KPL2-C30-430-PP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-PP001`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-090 — SLD-only asset not found in consumer list: KPL2-C30-430-CP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-CP001`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-091 — SLD-only asset not found in consumer list: KPL2-C30-430-FN001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-FN001`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-092 — SLD-only asset not found in consumer list: KPL2-C30-430-MX002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-MX002`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-093 — SLD-only asset not found in consumer list: KPL2-C30-430-FN002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-FN002`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-094 — SLD-only asset not found in consumer list: KPL2-C30-430-HT001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-HT001`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-095 — SLD-only asset not found in consumer list: KPL2-C30-430-CP002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-CP002`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-096 — SLD-only asset not found in consumer list: KPL2-C30-430-PK001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-PK001`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-097 — SLD-only asset not found in consumer list: KPL2-C30-430-HT002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-HT002`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-098 — SLD-only asset not found in consumer list: KPL2-C30-430-FN003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-FN003`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-099 — SLD-only asset not found in consumer list: KPL2-C30-430-PK002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-PK002`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-100 — SLD-only asset not found in consumer list: KPL2-C30-430-FN004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-FN004`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-101 — SLD-only asset not found in consumer list: KPL2-C30-430-PK003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-PK003`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'PK'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-102 — SLD-only asset not found in consumer list: KPL2-C30-430-FN005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-FN005`
- Evidence: `{'visual_parent': 'KPL2-C30-430-LV03-MCC05', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-103 — SLD-only asset not found in consumer list: KPL2-C30-430-MV001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-MV001`
- Evidence: `{'visual_parent': 'KPL2-C30-430-MV01-SWG01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-104 — SLD-only asset not found in consumer list: KPL2-C30-430-MV002
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-MV002`
- Evidence: `{'visual_parent': 'KPL2-C30-430-MV01-SWG01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-105 — SLD-only asset not found in consumer list: KPL2-C30-430-MV003
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-MV003`
- Evidence: `{'visual_parent': 'KPL2-C30-430-MV01-SWG01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-106 — SLD-only asset not found in consumer list: KPL2-C30-430-MV004
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-MV004`
- Evidence: `{'visual_parent': 'KPL2-C30-430-MV01-SWG01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-107 — SLD-only asset not found in consumer list: KPL2-C30-430-MV005
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-C30-430-MV005`
- Evidence: `{'visual_parent': 'KPL2-C30-430-MV01-SWG01', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-108 — SLD-only asset not found in consumer list: KPL2-A10-410-PP009
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-A10-410-PP009`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-DB01', 'asset_type': 'HE'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-109 — SLD-only asset not found in consumer list: KPL2-Z90-999-PP001
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-Z90-999-PP001`
- Evidence: `{'visual_parent': 'KPL2-Z90-999-LV99-MCC99', 'asset_type': 'MAA'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-110 — SLD-only asset not found in consumer list: KPL2-X40-440-LV04-MCC09
- Severity: **medium**
- Confidence: **1.00**
- Item: `KPL2-X40-440-LV04-MCC09`
- Evidence: `{'visual_parent': 'KPL2-A10-410-LV01-SWBD01', 'asset_type': 'MCC'}`
- Recommendation: Verify whether this is a spare, future feeder, or missing consumer-list row.

### SLD-111 — Parent mismatch for KPL2-B20-420-LV02-MCC04
- Severity: **high**
- Confidence: **1.00**
- Item: `KPL2-B20-420-LV02-MCC04`
- Evidence: `{'consumer_parent': 'KPL2-B20-420-LV02-SWBD02', 'sld_parent': 'KPL2-C30-430-LV03-SWBD03'}`
- Recommendation: Resolve parent assignment between consumer list and SLD drawing.

## Limitations

SingleLineIQ performs document consistency review and connected-load aggregation. It does not perform load flow, short-circuit, protection coordination, motor starting, or arc-flash studies.