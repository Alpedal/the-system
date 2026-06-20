#!/usr/bin/env python3
"""
Spike 004 — GPU-telemetri: Testar om nvidia-ml-py kan läsa VRAM-data.

Kör med: uv run python test_gpu_telemetry.py
"""

import json
import sys
import time
import traceback


def main():
    print("[SPIKE 004] GPU-telemetri — nvidia-ml-py test", flush=True)
    print("=" * 60, flush=True)

    # ---------------------------------------------------------------
    # 1. Försök importera och initiera pynvml
    # ---------------------------------------------------------------
    try:
        import pynvml
        print("[OK] nvidia-ml-py importerad som pynvml", flush=True)
    except ImportError:
        print("[FAIL] Kunde inte importera pynvml. Installerar...", flush=True)
        print("[INFO] Användaren bör köra: uv add nvidia-ml-py", flush=True)
        sys.exit(1)

    try:
        pynvml.nvmlInit()
        print("[OK] nvmlInit() lyckades", flush=True)
    except pynvml.NVMLError_LibraryNotFound:
        print("[FAIL] NVML-biblioteket hittades inte. Ingen NVIDIA-drivrutin installerad?", flush=True)
        sys.exit(1)
    except pynvml.NVMLError as e:
        print(f"[FAIL] nvmlInit() misslyckades: {e}", flush=True)
        sys.exit(1)

    # ---------------------------------------------------------------
    # 2. Hämta GPU-statistik och streama som JSON
    # ---------------------------------------------------------------
    try:
        device_count = pynvml.nvmlDeviceGetCount()
        print(f"[OK] Hittade {device_count} GPU(er)", flush=True)
    except pynvml.NVMLError as e:
        print(f"[FAIL] nvmlDeviceGetCount() misslyckades: {e}", flush=True)
        pynvml.nvmlShutdown()
        sys.exit(1)

    for i in range(device_count):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            # Vissa äldre drivrutiner returnerar bytes
            if isinstance(name, bytes):
                name = name.decode("utf-8")

            # Total VRAM
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            vram_total_mb = mem_info.total / (1024 * 1024)
            vram_used_mb = mem_info.used / (1024 * 1024)
            vram_free_mb = mem_info.free / (1024 * 1024)

            # GPU-utilisering (stöds kanske inte på äldre GTX-kort)
            try:
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                gpu_util_pct = util.gpu
            except pynvml.NVMLError:
                gpu_util_pct = None

            # Temperatur
            try:
                temp = pynvml.nvmlDeviceGetTemperature(
                    handle, pynvml.NVML_TEMPERATURE_GPU
                )
            except pynvml.NVMLError:
                temp = None

            record = {
                "gpu_index": i,
                "name": name,
                "vram_total_mb": round(vram_total_mb, 1),
                "vram_used_mb": round(vram_used_mb, 1),
                "vram_free_mb": round(vram_free_mb, 1),
                "vram_used_pct": round(
                    (mem_info.used / mem_info.total) * 100, 1
                ),
                "gpu_util_pct": gpu_util_pct,
                "temperature_c": temp,
                "timestamp": time.time(),
            }

            print(json.dumps(record, indent=2), flush=True)

        except pynvml.NVMLError as e:
            print(
                json.dumps(
                    {
                        "gpu_index": i,
                        "error": str(e),
                        "timestamp": time.time(),
                    }
                ),
                flush=True,
            )

    # ---------------------------------------------------------------
    # 3. Städa upp
    # ---------------------------------------------------------------
    pynvml.nvmlShutdown()
    print("\n[SPIKE 004] Klar. nvmlShutdown() anropad.", flush=True)


if __name__ == "__main__":
    main()
