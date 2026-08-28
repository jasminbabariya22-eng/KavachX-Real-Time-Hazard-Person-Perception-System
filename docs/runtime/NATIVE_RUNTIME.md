# Native C++ Worker Daemon Architecture

## 1. Overview
The native worker (`native/worker/kawach_worker`) is a C++11 daemon that initializes the Qualcomm QNN HTP runtime, opens a FastRPC channel to the DSP (`/dev/fastrpc-cdsp`), and serves inference requests over `/tmp/kawach_worker.sock`.

---

## 2. Core Implementation Files

| File | Purpose | Key Functions / Classes |
| :--- | :--- | :--- |
| `main.cpp` | Daemon entrypoint, CLI parser, signal handling, and socket server. | `main()`, `run_server()`, `handle_client()` |
| `qnn_inference.cpp` | QNN SDK C API wrapper, context deserialization, and FastRPC execution. | `QnnInferenceEngine::initialize()`, `execute()` |
| `qnn_inference.hpp` | Header declarations and QNN tensor structs. | `QnnInferenceEngine` |
| `ipc_handler.cpp` | Framing parser, request validator, and response packager. | `IpcHandler::read_request()`, `send_response()` |
| `ipc_handler.hpp` | Binary protocol header constants and structures. | `RequestHeader`, `ResponseHeader` |
| `Makefile` | Native compilation script linking `libQnnHtp.so`. | Clean, multi-threaded build target |
