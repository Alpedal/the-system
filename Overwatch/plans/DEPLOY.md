# Commander Igris — Deployment & Remote Tunneling Guide

Detta dokument beskriver hur man driftsätter **Commander Igris** API-backend och det tillhörande Solo System Web UI, samt hur man exponerar tjänsten säkert för fjärråtkomst (t.ex. för William, Alpedal och andra) med hjälp av **Cloudflare Tunnels** eller **Tailscale Funnel**.

---

## 1. Förutsättningar (Prerequisites)

Följande krävs på värddatorn (Alpedals superdator):
- **Hårdvara**: NVIDIA GPU med CUDA-stöd (specad för RTX 3090 24GB VRAM) och minst 64GB system-RAM.
- **Programvara**: Python 3.11 eller 3.13 installerat, samt pakethanteraren `uv` för snabb installation.
- **Ollama**: Installerat och igång (`localhost:11434`). Ladda ner nödvändiga modeller:
  ```bash
  ollama pull qwen2.5-coder:32b
  ollama pull llama3.1:8b
  ```

---

## 2. Installation & Konfiguration

Klonprojektet innehåller en `requirements.txt`. Installera alla nödvändiga beroenden i ditt system- eller virtuella python-miljö med `uv`:

```bash
uv pip install -r igris/requirements.txt
```

### Konfiguration av miljövariabler
Innan servern startas bör du ställa in en säker API-token för att förhindra obehörig åtkomst:

**I PowerShell (Windows):**
```powershell
$env:IGRIS_API_TOKEN="ditt-superhemliga-lösenord"
```

**I Bash (Linux/macOS):**
```bash
export IGRIS_API_TOKEN="ditt-superhemliga-lösenord"
```

*Om ingen token anges styrs säkerheten av default-token `igris-dev-token`.*

---

## 3. Starta Backend & Frontend

Starta FastAPI-servern med hjälp av uvicorn. Servern lyssnar på port `8000` som standard och serverar automatiskt det statiska Solo System Web UI på `/`:

```bash
py -m uvicorn igris.api.main:app --host 127.0.0.1 --port 8000 --reload
```

Verifiera att du kan nå gränssnittet lokalt på `http://localhost:8000/`. Logga in genom att ange din token längst ner i sidopanelen (`Systeminställningar`).

---

## 4. Exponering via Cloudflare Tunnel (Rekommenderas)

En **Cloudflare Tunnel** låter dig exponera den lokala porten `8000` på en offentlig HTTPS-domän (t.ex. `igris.dindomän.com`) utan att behöva öppna portar i din hemrouter eller konfigurera DDNS.

### Steg 1: Installera Cloudflare CLI (cloudflared)
**På Windows (via winget):**
```powershell
winget install Cloudflare.cloudflared
```

### Steg 2: Logga in på Cloudflare
Kör följande kommando och följ länken för att auktorisera din domän:
```bash
cloudflared tunnel login
```

### Steg 3: Skapa en ny tunnel
Skapa en tunnel och ge den ett namn (t.ex. `igris-tunnel`):
```bash
cloudflared tunnel create igris-tunnel
```
*Detta genererar ett tunnel-ID och sparar en autentiseringsfil (.json) i din hemkatalog under `~/.cloudflare/`.*

### Steg 4: Konfigurera DNS-rutt
Koppla din tunnel till en underdomän:
```bash
cloudflared tunnel route dns igris-tunnel igris.dindomän.com
```

### Steg 5: Skapa konfigurationsfil (config.yml)
Skapa en konfigurationsfil under `%USERPROFILE%\.cloudflare\config.yml` (Windows) eller `~/.cloudflare/config.yml` (Linux) med följande innehåll:

```yaml
tunnel: <TUNNEL_ID_HÄRI>
credentials-file: C:\Users\<ANVÄNDARE>\.cloudflare\<TUNNEL_ID_HÄRI>.json

ingress:
  - hostname: igris.dindomän.com
    service: http://localhost:8000
  - service: http_status:404
```

### Steg 6: Kör tunneln
Starta tunneln för att börja vidarebefordra trafik:
```bash
cloudflared tunnel run igris-tunnel
```
Fjärranvändare kan nu nå ditt Solo System gränssnitt på `https://igris.dindomän.com`!

---

## 5. Exponering via Tailscale Funnel (Alternativ)

Om du redan använder Tailscale kan du använda **Tailscale Funnel** för att exponera tjänsten på din tailnet-adress offentligt.

### Steg 1: Installera Tailscale
Ladda ner och installera Tailscale på värddatorn, anslut till ditt nätverk.

### Steg 2: Konfigurera Tailscale Serve
Kör följande kommando för att starta portvidarebefordran internt i bakgrunden:
```bash
tailscale serve --bg tcp:8000
```

### Steg 3: Aktivera Funnel
Exponera porten för hela internet via din Tailscale maskin-URL:
```bash
tailscale funnel 8000 on
```
Tjänsten är nu nåbar offentligt via den tilldelade Tailscale-länken (t.ex. `https://supercomputer.tailnet-id.ts.net`).
