# Test Strategy & Validation Architecture

## 1. Multi-Tier Testing Methodology

```text
┌────────────────────────────────────────────────────────┐
│  Tier 4: Live Bounded Streaming & Concurrency Tests     │
│  (tests/streaming/test_live_stream.py)                 │
├────────────────────────────────────────────────────────┤
│  Tier 3: Stream Pipeline Integration Tests             │
│  (tests/integration/test_pipeline_integration.py)      │
├────────────────────────────────────────────────────────┤
│  Tier 2: Hardware DSP & FastRPC Regression Tests        │
│  (tests/hardware/test_htp_inference.py)                │
├────────────────────────────────────────────────────────┤
│  Tier 1: Pre-Flight Integrity & Model SHA256 Check     │
│  (tools/model_inspect.py)                              │
└────────────────────────────────────────────────────────┘
```

---

## 2. Test Execution Commands

```bash
# Run all automated tests via Makefile
make test

# Or run individual tiers:
python3 tests/hardware/test_htp_inference.py
python3 tests/integration/test_pipeline_integration.py
python3 tests/streaming/test_live_stream.py
```
