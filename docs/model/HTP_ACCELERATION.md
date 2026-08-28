# Qualcomm Hexagon v68 HTP Hardware Acceleration

## 1. Hardware Architecture
- **Processor SoC:** Qualcomm QCS6490 (8-core Kryo 670 CPU up to 2.7 GHz, Adreno 643 GPU).
- **Neural Hardware Accelerator:** Qualcomm Hexagon v68 HTP (Hexagon Tensor Processor) DSP.
- **Transport Driver:** Qualcomm FastRPC (`/dev/fastrpc-cdsp`).
- **Software Runtime:** Qualcomm QAIRT / QNN SDK 2.47.0.260601.

---

## 2. FastRPC Device Node Permissions
- **Device Path:** `/dev/fastrpc-cdsp`
- **Ownership & Permissions:** `root:render` (`0660`, GID `993`).
- **User Configuration:** The active service user (`work_user2`) is a verified member of the `render` group (`GID 993`).
- **Admin Action Required:** **NO** (all permissions are established and verified).

---

## 3. Zero CPU Fallback Verification
During inference, QNN loads `libQnnHtp.so` and binds all graph nodes directly to the Hexagon DSP. No sub-graphs are partitioned to the CPU or GPU, ensuring maximum power efficiency and leaving CPU cores idle for video ingestion.
