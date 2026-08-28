# Model Integrity & Tamper Protection

## 1. Cryptographic Checksum Enforcement
During pre-flight initialization, `tools/service_manager.py` computes the SHA256 checksum of the production context binary before spawning the worker:

- **Expected SHA256:** `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc`
- **Tamper Behavior:** If the file checksum deviates, startup aborts immediately and the health state is marked `FAILED`.
