# Developer Onboarding & Contribution Guide

## 1. Local Development Workflow
1. **Clone Repository:**
   ```bash
   git clone https://github.com/jasminbabariya22-eng/KavachX-Real-Time-Hazard-Person-Perception-System.git
   cd KavachX
   ```
2. **Install Local Dependencies:**
   ```bash
   pip install -e .
   ```
3. **Execute Remote Target Tests:**
   ```powershell
   python tools/target_runner.py "cd /home/work_user2/kawachx_task && make test"
   ```
