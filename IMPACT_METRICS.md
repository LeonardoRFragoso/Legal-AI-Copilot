# Impact Metrics

## Overview

The Legal AI Copilot estimates productivity gains from AI-assisted contract analysis. Metrics are calculated from persisted `AnalysisRecord` entries and displayed on the **Insights** dashboard.

## API Endpoint

```
GET /metrics/impact
```

Returns aggregated metrics for the authenticated user (ADMIN sees global, others see own data).

## Metrics Calculated

### Core Metrics
- **documents_total**: Total documents owned by user
- **analyses_total**: Total analysis records
- **approval_rate**: Percentage of analyses approved (APPROVED / total * 100)
- **average_confidence_score**: Mean confidence score across all analyses

### Breakdowns
- **analyses_by_type**: Count per analysis type (SUMMARY, EXTRACTION, etc.)
- **reviews_by_status**: Count per status (GENERATED, PENDING_REVIEW, APPROVED, etc.)
- **risks_by_severity**: Count per risk severity (low, medium, high, critical)
- **automations_by_status**: Count per automation run status

### Productivity Estimates
- **estimated_manual_minutes**: Sum of estimated manual processing time for all analyses
- **estimated_time_saved_minutes**: Sum of estimated time saved (manual - actual processing)
- **estimated_time_saved_hours**: Converted to hours
- **average_processing_duration_ms**: Mean processing time in milliseconds

### Operational
- **failed_webhooks**: Count of automation runs with failed webhook delivery

## Configuration

Manual time estimates are configurable via environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `ESTIMATED_MANUAL_SUMMARY_MINUTES` | 30 | Manual summary time |
| `ESTIMATED_MANUAL_EXTRACTION_MINUTES` | 45 | Manual extraction time |
| `ESTIMATED_MANUAL_COMPARISON_MINUTES` | 90 | Manual comparison time |
| `ESTIMATED_MANUAL_QA_MINUTES` | 15 | Manual Q&A time |
| `ESTIMATED_MANUAL_RISK_ANALYSIS_MINUTES` | 120 | Manual risk analysis time |

## Formula

```
estimated_time_saved = estimated_manual_minutes - (processing_duration_ms / 60000)
```

If `processing_duration_ms` is not available, `estimated_time_saved = estimated_manual_minutes`.

## Important Notice

All productivity metrics are **estimates** based on configurable reference values for manual processing times. They are illustrative for MVP demonstration purposes and should not be used as definitive productivity measurements without calibration against real workflow data.

## Frontend

The **Insights** page (`/insights`) displays:
- Top metric cards (documents, analyses, time saved, approval rate)
- Analyses by type (bar chart)
- Reviews by status (list)
- Risks by severity (badges)
- Automations by status (list)
- Productivity estimate detail (manual time, saved time, confidence)
- Estimation notice disclaimer
