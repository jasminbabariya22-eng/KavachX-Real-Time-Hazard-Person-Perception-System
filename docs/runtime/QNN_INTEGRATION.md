# Qualcomm QNN SDK C API Integration

## 1. Context Deserialization Flow
The native worker loads the pre-compiled context binary directly using the QNN System interface:

```cpp
// Initialize QNN System Function Pointers
QnnSystemInterface_t sysInterface;
QnnSystemInterface_getProviders(&sysInterface);

// Deserialize Context Binary
Qnn_ContextHandle_t contextHandle;
sysInterface.systemContextCreateFromBinary(
    binaryBuffer, binarySize, &contextHandle, ...
);
```

All graph inputs and outputs are registered in static RPCMem shared buffers, ensuring zero-copy tensor transfers between CPU and DSP during live inference.
