# Alert Event Pipeline & Debouncing

```mermaid
flowchart TD
    DET["Raw Detections from NMS"] --> CONF_FILTER{"Confidence >= 0.25?"}
    
    CONF_FILTER -->|No| DROP["Discard Low-Confidence Detection"]
    CONF_FILTER -->|Yes| MAP_CLS["Map Category:\n- Class 0 -> FIRE\n- Class 1 -> SMOKE\n- Class 2 -> PERSON"]
    
    MAP_CLS --> DEBOUNCE{"Time since last event > 3.0s?"}
    
    DEBOUNCE -->|No (Cooldown Active)| SUPPRESS["Update Tracking State\n(Suppress Duplicate Alarm)"]
    DEBOUNCE -->|Yes| DISPATCH["Dispatch Alert Event:\n- FIRE -> Severity: CRITICAL\n- SMOKE -> Severity: WARNING\n- PERSON -> Severity: WARNING"]
```
