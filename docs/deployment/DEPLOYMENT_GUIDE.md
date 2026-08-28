# Turnkey Deployment Guide

## 1. Prerequisites & Environment Setup

### 1.1 Target Hardware & Operating System
- **Hardware:** Qualcomm QCS6490 (Radxa Dragon Q6490 / Kavach-EdgeBox).
- **OS:** Linux 6.6 ARM64 (`aarch64-linux-gnu`).
- **FastRPC Permissions:** User must belong to `render` group (GID `993`):
  ```bash
  sudo usermod -a -G render $USER
  ```

### 1.2 Required Environment Variables
Add to `~/.bashrc` on the target EdgeBox:
```bash
export ADSP_LIBRARY_PATH="/home/devuser/qairt/2.47.0.260601/lib/hexagon-v68/unsigned;/vendor/dsp/cdsp;/vendor/lib/rfsa/adsp;/dsp"
export LD_LIBRARY_PATH="/home/devuser/qairt/2.47.0.260601/lib/aarch64-ubuntu-gcc9.4:$LD_LIBRARY_PATH"
```

---

## 2. Installation & Verification

### Step 1: Run Turnkey Installer
```bash
bash deployment/install.sh
```

### Step 2: Build Native Worker
```bash
make build
```

### Step 3: Start Production Daemon Service
```bash
python3 tools/service_manager.py start
```

### Step 4: Verify Service Health
```bash
cat /tmp/kawach_health.json
```

### Step 5: Run Automated Regression Tests
```bash
make test
```

### Step 6: Launch Live Interactive Demonstration
```bash
make demo
```
