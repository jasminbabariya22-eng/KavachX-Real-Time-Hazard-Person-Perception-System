# Hardware DSP & FastRPC Testing

## 1. Hardware Test Suite (`tests/hardware/test_htp_inference.py`)
Verifies direct communication with the Qualcomm Hexagon v68 HTP DSP:
1. Tests FastRPC connection over `/dev/fastrpc-cdsp`.
2. Validates QNN HTP backend execution (`libQnnHtp.so`).
3. Confirms **0 CPU fallback layers** during full model forward passes.
