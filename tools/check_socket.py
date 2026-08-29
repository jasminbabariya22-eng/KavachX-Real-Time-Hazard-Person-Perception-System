import socket
import sys

try:
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/tmp/kawach_worker.sock")
    print("SUCCESS: Connected to /tmp/kawach_worker.sock")
    s.close()
except Exception as e:
    print(f"FAILED: {e}")
