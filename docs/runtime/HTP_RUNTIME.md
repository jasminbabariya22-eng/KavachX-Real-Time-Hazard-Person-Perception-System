# Qualcomm Hexagon HTP Runtime Architecture

## 1. Runtime Layer Interactions
- **SoC Platform:** Qualcomm QCS6490.
- **DSP Core:** Qualcomm Hexagon v68 HTP (Hexagon Tensor Processor).
- **Transport Driver:** Qualcomm FastRPC (`/dev/fastrpc-cdsp`).
- **Software Runtime:** Qualcomm QAIRT / QNN SDK 2.47.0.260601 (`libQnnHtp.so`, `libQnnSystem.so`).

---

## 2. FastRPC Device Node Permissions
- **Device Node:** `/dev/fastrpc-cdsp`
- **Ownership & Mode:** `root:render` (`0660`, GID `993`).
- **User Group Membership:** Active service user `work_user2` is a verified member of group `render` (GID `993`).
