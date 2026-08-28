# Native C++ Worker Architecture

## 1. Architecture & Lifecycle
`native/worker/kawach_worker` is a compiled C++11 daemon providing deterministic, low-overhead inference over a UNIX domain stream socket.

---

## 2. Key Modules
- `main.cpp`: Entry point, command line parser, signal handling (`SIGINT`, `SIGTERM`), socket server loop.
- `qnn_inference.cpp` / `qnn_inference.hpp`: Wraps QNN SDK C APIs, manages context binary deserialization, and executes FastRPC calls.
- `ipc_handler.cpp` / `ipc_handler.hpp`: Non-blocking socket listener, packet framing validator, and response packager.
