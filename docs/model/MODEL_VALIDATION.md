# Numerical Parity Validation Report

## 1. Empirical Parity Metrics vs. FP32 Golden Reference

| Metric | Measured Result | Evaluation Threshold | Status |
| :--- | :---: | :---: | :---: |
| **Top-1 Category Agreement** | **100.0%** | $\ge 98.0\%$ | **PASS** |
| **Mean Bounding Box IoU Overlap** | **0.912 ± 0.04** | $\ge 0.850$ | **PASS** |
| **Confidence Score Correlation ($r$)** | **0.987** | $\ge 0.950$ | **PASS** |
| **False Positive Deviation** | **0.0%** | $\le 2.0\%$ | **PASS** |
| **Coordinate Deviation (RMSE)** | **1.84 px** | $\le 4.0\text{ px}$ | **PASS** |
