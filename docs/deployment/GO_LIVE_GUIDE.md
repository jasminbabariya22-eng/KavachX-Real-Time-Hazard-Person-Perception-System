# Go-Live & Commissioning Guide

## 1. Pre-Commissioning Checklist
- [x] FastRPC Device node `/dev/fastrpc-cdsp` accessible by service user (`render` GID `993`).
- [x] QNN HTP runtime libraries (`libQnnHtp.so`) linked in `LD_LIBRARY_PATH`.
- [x] Model checksum matches `b7868a8c436fcf723fea7f95b3dcfd6f131fbe8ddb02ddf103addbe351dafabc`.
- [x] Native worker builds cleanly with 0 warnings/errors (`make build`).
- [x] Automated regression test suite passes 100% (`make test`).
- [x] Live interactive camera demo completes gracefully (`make demo`).
