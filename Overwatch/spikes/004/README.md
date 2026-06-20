# Spike 004 — GPU-telemetri (nvidia-ml-py)

## Syfte

Testa om [nvidia-ml-py](https://pypi.org/project/nvidia-ml-py/) kan installeras och läsa
VRAM-data från en NVIDIA GPU, samt streama statistiken som JSON.

---

## Given / When / Then

### Scenario 1: Installation och import

```
Given en miljö med uv och Python 3.11
When  vi kör "uv run --with nvidia-ml-py python"
Then  pynvml importeras utan fel
```

**Resultat:** ✅ PASS — `uv run --with nvidia-ml-py` installerar paketet på 42 ms och import fungerar.

### Scenario 2: NVML-biblioteket finns

```
Given en Windows-maskin med NVIDIA-drivrutin
When  vi letar efter nvml.dll
Then  filen finns i C:\Windows\System32\
```

**Resultat:** ✅ PASS — `nvml.dll` (1.3 MB) finns i `C:\Windows\System32\` samt två kopior i DriverStore.

### Scenario 3: GPU-statistik (VRAM, GPU-util)

```
Given en NVIDIA GPU (GTX 980 Ti / RTX 3090)
When  vi anropar nvmlInit() följt av nvmlDeviceGetMemoryInfo()
Then  vi får VRAM-total, VRAM-used, VRAM-free som JSON
```

**Resultat:** ❌ **BLOCKED** — `nvmlInit()` returnerar `NVMLError_NoPermission: Insufficient Permissions`.

- `nvml.dll` kan laddas via `ctypes.CDLL("nvml.dll")` ✅
- `nvmlInit_v2()` returnerar felkod 4 (`NVML_ERROR_NO_PERMISSION`) ❌
- NVIDIA-drivrutinen är installerad (`nvidia-smi.exe` finns) ✅
- Orsak: NVML på Windows kräver **Administratörsrättigheter** för att initiera

---

## Verkliga testdata (icke-admin)

Ingen GPU-data kunde läsas utan admin. Med admin skulle följande finnas:

```json
{
  "gpu_index": 0,
  "name": "NVIDIA GeForce GTX 980 Ti",
  "vram_total_mb": 4096.0,
  "vram_used_mb": "<varierar>",
  "vram_free_mb": "<varierar>",
  "vram_used_pct": "<varierar>",
  "gpu_util_pct": "<0-100 eller None>",
  "temperature_c": "<celcius eller None>",
  "timestamp": 1718000000.0
}
```

---

## Verktyg som skapats

| Fil | Syfte |
|---|---|
| `test_gpu_telemetry.py` | Throwaway-skript: installerar nvidia-ml-py, försöker läsa GPU-data, streamar JSON |
| `diagnose_gpu_telemetry.py` | Diagnostik: testar NVML DLL, ctypes, pynvml och rapporterar blockerare |
| `admin_test.py` | Test för att köras som Administrator (skriver till %TEMP%) |
| `run_admin.ps1` | PowerShell-wrapper för att starta admin_test.py med förhöjda rättigheter |
| `README.md` | Denna fil |

---

## Verdict

```
╔══════════════════════════════════════════════════════════╗
║  VERDICT: BLOCKED                                        ║
║                                                          ║
║  nvidia-ml-py fungerar — MEN kräver admin på Windows.    ║
║                                                          ║
║  Vad som krävs:                                          ║
║  • NVIDIA GPU + drivrutin (finns ✅)                     ║
║  • nvidia-ml-py installerat (funkar ✅)                  ║
║  • Python kört som Administrator (krävs ❌)               ║
║                                                          ║
║  Rekommendation:                                         ║
║  På Alpedals maskin (RTX 3090) — testa om admin krävs    ║
║  där också. Om ja: Overwatch-tjänsten måste köras med    ║
║  förhöjda rättigheter, eller använd nvidia-smi --query    ║
║  via subprocess som fallback (kräver också admin).        ║
╚══════════════════════════════════════════════════════════╝
```

---

## Alternativ

1. **Administratörsläge** — Kör python- eller uv-tjänsten som Administrator (högerklicka → Run as administrator). Då fungerar `pynvml.nvmlInit()` fullt ut.

2. **nvidia-smi CLI** — Fallback: anropa `nvidia-smi --query-gpu=... --format=csv` via `subprocess`. Kräver också admin på denna maskin.

3. **Linux** — NVML kräver INTE root på Linux (endast read-permission på `/dev/nvidia*`). Om Overwatch tjänsten flyttas till Linux är detta inget problem.

---

*Spike genomförd: 2026-06-20*
*Maskin: William Perssons dator (GTX 980 Ti 4GB)*
*Målmaskin: Alpedals maskin (RTX 3090 24GB)*
