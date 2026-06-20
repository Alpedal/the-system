#!/usr/bin/env python3
"""
Spike 004 — GPU-telemetri: Diagnostisk test för nvidia-ml-py.

Testar olika initieringssätt och rapporterar vad som krävs.
"""

import json
import sys
import os
import time
import ctypes


def check_nvml_library():
    """Kontrollera om NVML-biblioteket finns på systemet."""
    print("\n--- 1. NVML-biblioteket ---", flush=True)
    possible_paths = [
        "C:/Windows/System32/nvml.dll",
        "C:/Windows/System32/DriverStore/FileRepository/nv_dispi.inf_amd64_6548260a81e093a0/nvml.dll",
        "C:/Windows/System32/DriverStore/FileRepository/nv_dispig.inf_amd64_f4c7a2fd13e0f763/nvml.dll",
    ]
    for p in possible_paths:
        exists = os.path.isfile(p)
        size = os.path.getsize(p) if exists else 0
        print(f"  {'[OK]' if exists else '[--]'} {p} ({size/1024/1024:.1f} MB)" if exists else f"  {'[--]'} {p}", flush=True)

    # Försök ladda med ctypes
    try:
        lib = ctypes.CDLL("nvml.dll")
        print(f"  [OK] nvml.dll kunde laddas med ctypes (handle: {lib})", flush=True)
        return True
    except Exception as e:
        print(f"  [FAIL] nvml.dll kunde inte laddas med ctypes: {e}", flush=True)
        return False


def check_nvidia_driver():
    """Kontrollera NVIDIA-drivrutin via Windows API."""
    print("\n--- 2. NVIDIA-drivrutin ---", flush=True)
    try:
        import win32api
        # Detta är en enkel kontroll
        print("  [OK] win32api tillgängligt", flush=True)
    except ImportError:
        # Kolla via DISPLAY-registryt eller Device Manager
        pass

    # Kolla via nvidia-smi (om tillgängligt)
    nv_smi = os.path.isfile("C:/Windows/System32/nvidia-smi.exe")
    print(f"  {'[OK]' if nv_smi else '[--]'} nvidia-smi.exe finns: {nv_smi}", flush=True)

    # Kolla driver version via NVML
    try:
        lib = ctypes.CDLL("nvml.dll")
        # nvmlInit_v2
        lib.nvmlInit_v2.restype = ctypes.c_uint
        ret = lib.nvmlInit_v2()
        if ret == 0:
            print("  [OK] nvmlInit_v2 via ctypes lyckades!", flush=True)
            # Get driver version
            buf = ctypes.create_string_buffer(80)
            lib.nvmlSystemGetDriverVersion(ctypes.byref(buf), ctypes.c_uint(80))
            print(f"  [OK] Driver version: {buf.value.decode()}", flush=True)
            lib.nvmlShutdown()
            return True
        else:
            error_codes = {
                1: "NVML_ERROR_UNINITIALIZED",
                2: "NVML_ERROR_INVALID_ARGUMENT",
                3: "NVML_ERROR_NOT_SUPPORTED",
                4: "NVML_ERROR_NO_PERMISSION",
                5: "NVML_ERROR_ALREADY_INITIALIZED",
                6: "NVML_ERROR_NOT_FOUND",
                7: "NVML_ERROR_INSUFFICIENT_SIZE",
                8: "NVML_ERROR_INSUFFICIENT_POWER",
                9: "NVML_ERROR_DRIVER_NOT_LOADED",
                10: "NVML_ERROR_TIMEOUT",
                11: "NVML_ERROR_IRQ_ISSUE",
                12: "NVML_ERROR_LIBRARY_NOT_FOUND",
                13: "NVML_ERROR_FUNCTION_NOT_FOUND",
            }
            err_name = error_codes.get(ret, f"UNKNOWN({ret})")
            print(f"  [FAIL] nvmlInit_v2 returerade {ret} ({err_name})", flush=True)
            return False
    except Exception as e:
        print(f"  [FAIL] ctypes-försök misslyckades: {e}", flush=True)
        return False


def test_pynvml():
    """Testa nvidia-ml-py (pynvml) ordentligt."""
    print("\n--- 3. nvidia-ml-py (pynvml) ---", flush=True)

    try:
        import pynvml
        print("  [OK] pynvml importerad", flush=True)
    except ImportError as e:
        print(f"  [FAIL] Kan inte importera pynvml: {e}", flush=True)
        return

    try:
        pynvml.nvmlInit()
        print("  [OK] nvmlInit() lyckades", flush=True)
    except pynvml.NVMLError_NoPermission as e:
        print(f"  [FAIL] nvmlInit(): {e}", flush=True)
        print("  [INFO] Lösning: Kör python som Administrator (högerklicka → Run as admin)", flush=True)
        print("  [INFO] ctypes-försöket gav felkod 4 = NVML_ERROR_NO_PERMISSION", flush=True)
        return
    except AttributeError:
        # fallback om exception-klassen inte finns i äldre pynvml
        try:
            pynvml.nvmlInit()
        except Exception as e:
            print(f"  [FAIL] nvmlInit(): {e}", flush=True)
            print("  [INFO] Lösning: Kör python som Administrator", flush=True)
            return
    except pynvml.NVMLError_LibraryNotFound as e:
        print(f"  [FAIL] nvmlInit(): {e} — Ingen NVIDIA-drivrutin", flush=True)
        return
    except pynvml.NVMLError as e:
        print(f"  [FAIL] nvmlInit(): {e}", flush=True)
        return

    # Om vi kom hit, läs GPU-data
    try:
        count = pynvml.nvmlDeviceGetCount()
        print(f"  [OK] GPU(er) hittade: {count}", flush=True)
    except pynvml.NVMLError as e:
        print(f"  [FAIL] nvmlDeviceGetCount(): {e}", flush=True)
        pynvml.nvmlShutdown()
        return

    for i in range(count):
        record = {"gpu_index": i}
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode("utf-8")
            record["name"] = name
            print(f"\n  GPU {i}: {name}", flush=True)

            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            record["vram_total_mb"] = round(mem.total / 1048576, 1)
            record["vram_used_mb"] = round(mem.used / 1048576, 1)
            record["vram_free_mb"] = round(mem.free / 1048576, 1)
            record["vram_used_pct"] = round((mem.used / mem.total) * 100, 1)
            print(f"    VRAM: {record['vram_used_mb']:.1f} / {record['vram_total_mb']:.1f} MB ({record['vram_used_pct']:.1f}%)", flush=True)

            try:
                util = pynvml.nvmlDeviceGetUtilizationRates(handle)
                record["gpu_util_pct"] = util.gpu
                print(f"    GPU util: {util.gpu}%", flush=True)
            except pynvml.NVMLError:
                record["gpu_util_pct"] = None
                print("    GPU util: N/A (stöds ej)", flush=True)

            try:
                temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
                record["temperature_c"] = temp
                print(f"    Temp: {temp}°C", flush=True)
            except pynvml.NVMLError:
                record["temperature_c"] = None
                print("    Temp: N/A", flush=True)

            try:
                power = pynvml.nvmlDeviceGetPowerUsage(handle)
                record["power_mw"] = power
                print(f"    Power: {power} mW", flush=True)
            except pynvml.NVMLError:
                record["power_mw"] = None
                print("    Power: N/A", flush=True)

        except pynvml.NVMLError as e:
            record["error"] = str(e)

        record["timestamp"] = time.time()
        print(f"\n  JSON: {json.dumps(record)}", flush=True)

    pynvml.nvmlShutdown()
    print("\n  [OK] nvmlShutdown() anropad", flush=True)


def main():
    print("=" * 65, flush=True)
    print("SPIKE 004 — GPU-telemetri: Diagnostik", flush=True)
    print("=" * 65, flush=True)

    has_lib = check_nvml_library()
    worked_via_ctypes = check_nvidia_driver()
    test_pynvml()

    print("\n--- SAMMANFATTNING ---", flush=True)
    print(f"  NVML DLL finns:    {'JA' if has_lib else 'NEJ'}", flush=True)
    print(f"  ctypes init:       {'JA' if worked_via_ctypes else 'NEJ (kräver admin)'}", flush=True)
    print(f"  pynvml init:       Testad ovan", flush=True)

    if not has_lib:
        print("\n  [VERDICT] INVALIDATED — Ingen NVIDIA-drivrutin installerad.", flush=True)
        print("  Krävs: NVIDIA GPU + NVIDIA-drivrutin (inkl. NVML DLL)", flush=True)
    elif not worked_via_ctypes:
        print("\n  [VERDICT] BLOCKED — NVML DLL finns men kräver adminrättigheter.", flush=True)
        print("  Krävs: Kör python som Administrator (högerklicka → Run as admin)", flush=True)
    else:
        print("\n  [VERDICT] PASS — GPU-telemetri fungerar via NVML.", flush=True)

    print("=" * 65, flush=True)


if __name__ == "__main__":
    main()
