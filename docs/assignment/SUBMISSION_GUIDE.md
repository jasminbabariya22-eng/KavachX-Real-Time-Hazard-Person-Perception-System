# Evaluator Quickstart & Submission Guide

Welcome to the **KavachX** technical evaluation guide.

---

## 1. Quick Verification on Hardware (Qualcomm QCS6490)

Log into the EdgeBox via SSH:
```bash
ssh work_user2@ssh.kavachx.io
cd /home/work_user2/kawachx_task
```

### 1.1 Build Native NPU Worker
```bash
make build
```

### 1.2 Start Production Daemon Service
```bash
python3 tools/service_manager.py start
cat /tmp/kawach_health.json
```

### 1.3 Run Automated Regression Tests
```bash
make test
```

### 1.4 Launch Live Interactive Demo
```bash
make demo
```

---

## 2. Key Deliverable Locations
- **INT8 Production Context Binary:** `models/production/3class_calibrated_final.bin`
- **Native FastRPC C++ Worker:** `native/worker/`
- **Core Python Perception Package:** `src/kavachx/`
- **System Architecture Manual:** `docs/architecture/SYSTEM_ARCHITECTURE.md`
- **Numerical Validation Report:** `docs/model/NUMERICAL_VALIDATION.md`
