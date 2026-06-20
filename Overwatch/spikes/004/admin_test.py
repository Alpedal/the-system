"""
Quick admin-test: run this as Administrator to verify nvidia-ml-py works.
Writes output to a temp file because admin UAC can't use stdout redirection.
"""
import json, sys, os, time

OUT = os.path.join(os.environ.get("TEMP", "C:\\Temp"), "spike004_result.json")

def out(s):
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(s + "\n")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
# Clear previous
open(OUT, "w").close()

out("[ADMIN TEST] Starting nvidia-ml-py test...")

try:
    import pynvml
except ImportError:
    out("[ADMIN TEST] Installing nvidia-ml-py...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "nvidia-ml-py"], check=True)
    import pynvml

pynvml.nvmlInit()
count = pynvml.nvmlDeviceGetCount()
out(json.dumps({"gpu_count": count}))

for i in range(count):
    h = pynvml.nvmlDeviceGetHandleByIndex(i)
    name = pynvml.nvmlDeviceGetName(h)
    if isinstance(name, bytes): name = name.decode()
    mem = pynvml.nvmlDeviceGetMemoryInfo(h)
    d = {
        "gpu_index": i,
        "name": name,
        "vram_total_mb": round(mem.total / 1048576, 1),
        "vram_used_mb": round(mem.used / 1048576, 1),
        "vram_free_mb": round(mem.free / 1048576, 1),
        "vram_used_pct": round((mem.used / mem.total) * 100, 1),
    }
    try:
        util = pynvml.nvmlDeviceGetUtilizationRates(h)
        d["gpu_util_pct"] = util.gpu
    except:
        d["gpu_util_pct"] = None

    try:
        d["temperature_c"] = pynvml.nvmlDeviceGetTemperature(h, pynvml.NVML_TEMPERATURE_GPU)
    except:
        d["temperature_c"] = None

    d["timestamp"] = time.time()
    out(json.dumps(d))

pynvml.nvmlShutdown()
out("[ADMIN TEST] COMPLETE")

