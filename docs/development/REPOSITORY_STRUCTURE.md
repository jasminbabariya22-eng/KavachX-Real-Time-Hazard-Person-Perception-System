# Repository Architecture & Classification

## 1. Directory Tree & Roles

```text
KavachX/
├── README.md                          # Primary project overview & quickstart
├── LICENSE                            # Apache 2.0 License
├── Makefile                           # Target build, test, demo, and clean targets
├── pyproject.toml                     # Python packaging configuration
├── requirements.txt                   # Production Python dependencies
│
├── src/kavachx/                       # Authoritative Production Python Package
│   ├── inference/                     # Inference engine, DFL decoder, letterbox postprocessing
│   ├── pipeline/                      # Live stream pipeline, bounded queue, alert events
│   ├── capture/                       # Camera sources (V4L2, RTSP, Video file)
│   ├── ipc/                           # Framed binary socket protocol & client
│   ├── service/                       # Health inspection & daemon state
│   ├── config/                        # Production configuration loader
│   └── common/                        # Logging and utilities
│
├── native/worker/                     # Authoritative C++ FastRPC Worker Daemon
│   ├── main.cpp
│   ├── qnn_inference.cpp
│   ├── qnn_inference.hpp
│   ├── ipc_handler.cpp
│   ├── ipc_handler.hpp
│   └── Makefile
│
├── models/
│   ├── production/                    # 3class_calibrated_final.bin (26.8 MB INT8)
│   └── reference/                     # new_3class_best_FP32_htp_split.onnx
│
├── config/                            # production.json & kawach_worker.service
├── deployment/                        # install.sh, uninstall.sh, run_demo.sh
├── tests/                             # hardware/, integration/, streaming/
├── tools/                             # benchmark.py, live_camera_viewer.py, service_manager.py
├── docs/                              # Comprehensive technical documentation portal
└── archive/                           # Preserved historical development milestones
```
