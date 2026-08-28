# KavachX Process Architecture

## 1. Process & Memory Layout

```mermaid
flowchart TD
    subgraph HOST_OS["Host Operating System (Linux 6.6 ARM64)"]
        subgraph SUPERVISOR["Process 1: Service Supervisor (tools/service_manager.py)"]
            SUP_LOOP["Watchdog & Lifecycle Loop"]
            HEALTH_FILE["/tmp/kawach_health.json"]
            SUP_LOOP --> HEALTH_FILE
        end

        subgraph WORKER_PROC["Process 2: Native Worker Daemon (native/worker/kawach_worker)"]
            SOCK_LISTENER["UNIX Socket Acceptor Thread\n(/tmp/kawach_worker.sock)"]
            QNN_ENGINE["QNN HTP Context Manager"]
            FASTRPC_CHAN["FastRPC Channel (/dev/fastrpc-cdsp)"]
            SOCK_LISTENER --> QNN_ENGINE
            QNN_ENGINE --> FASTRPC_CHAN
        end

        subgraph PYTHON_APP["Process 3: Perception Pipeline (src/kavachx)"]
            THREAD_CAP["Thread 1: Capture Ingestion Loop"]
            QUEUE_MEM["Bounded Queue Buffer (maxsize=2)"]
            THREAD_INF["Thread 2: Inference & Alert Loop"]
            
            THREAD_CAP --> QUEUE_MEM
            QUEUE_MEM --> THREAD_INF
        end
    end

    subgraph DSP_PROC["Qualcomm Hexagon DSP Realm"]
        CDSP_EXEC["Hexagon v68 HTP Compute Engine\n- 100% Neural Network Evaluation\n- Zero Host Memory Allocation"]
    end

    SUP_LOOP -.->|Monitors PID| WORKER_PROC
    THREAD_INF <==>|UNIX Domain Socket| SOCK_LISTENER
    FASTRPC_CHAN <==>|FastRPC Kernel Driver| CDSP_EXEC
```

---

## 2. Process Isolation & Fault Boundaries
1. **Daemon Independence:** `kawach_worker` operates as a persistent daemon. Client terminations or camera stream failures do not terminate the FastRPC context or cause DSP resets.
2. **Memory Safety:** The C++ daemon pre-allocates QNN input/output RPCMem buffers during startup. No dynamic heap allocations occur during the per-frame inference loop.
3. **Supervisor Self-Healing:** If `kawach_worker` receives a `SIGKILL` or encounters an unhandled exception, `tools/service_manager.py` detects the dead PID, cleans the socket, and restarts the daemon within $2.0\text{ seconds}$.
