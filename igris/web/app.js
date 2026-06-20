const DEFAULT_TOKEN = "igris-dev-token";
let ws = null;
let reconnectTimer = null;

const tokenInput = document.querySelector("#tokenInput");
const saveToken = document.querySelector("#saveToken");
const apiStatus = document.querySelector("#apiStatus");
const syncText = document.querySelector("#syncText");
const msgsContainer = document.querySelector("#msgs");
const sendBtn = document.querySelector("#sendBtn");
const chatIn = document.querySelector("#chatIn");

// Helper to get authorization token
function getToken() {
  return localStorage.getItem("igris-api-token") || DEFAULT_TOKEN;
}

// Get authorization headers
function getHeaders() {
  return {
    "Authorization": `Bearer ${getToken()}`,
    "Content-Type": "application/json"
  };
}

// Update API Connection status pill
function setConnectionStatus(status) {
  if (status === "online") {
    apiStatus.textContent = "ONLINE";
    apiStatus.className = "status-tag";
    apiStatus.style.background = "rgba(99, 102, 241, 0.12)";
    apiStatus.style.borderColor = "var(--border-active)";
    apiStatus.style.color = "var(--system-blue)";
    syncText.textContent = "REDO";
    syncText.style.color = "var(--green)";
    document.querySelector("#hpFill").style.width = "100%";
  } else {
    apiStatus.textContent = "OFFLINE";
    apiStatus.className = "status-tag offline";
    apiStatus.style.background = "rgba(239, 68, 68, 0.1)";
    apiStatus.style.borderColor = "rgba(239, 68, 68, 0.25)";
    apiStatus.style.color = "var(--red)";
    syncText.textContent = "KOPPLAR FRÅN";
    syncText.style.color = "var(--red)";
    document.querySelector("#hpFill").style.width = "25%";
  }
}

// Connect to WebSockets for live status updates
function connectWebSocket() {
  if (ws) {
    ws.close();
  }

  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  // Support local development proxying / absolute mapping
  const wsUrl = `${protocol}//${window.location.host}/ws`;

  logger("Ansluter till WebSocket-kanalen...");
  ws = new WebSocket(wsUrl);

  ws.onopen = () => {
    logger("WebSocket ansluten.");
    setConnectionStatus("online");
    if (reconnectTimer) {
      clearInterval(reconnectTimer);
      reconnectTimer = null;
    }
  };

  ws.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data);
      if (payload.event === "status_update") {
        updateAgents(payload.data.agents);
        updateQuests(payload.data.tasks);
      }
    } catch (e) {
      console.error("Failed to parse WebSocket message:", e);
    }
  };

  ws.onclose = () => {
    logger("WebSocket-anslutning stängdes. Försöker återansluta...");
    setConnectionStatus("offline");
    if (!reconnectTimer) {
      reconnectTimer = setInterval(connectWebSocket, 3000);
    }
  };

  ws.onerror = (err) => {
    console.error("WebSocket error:", err);
  };
}

// Append logs/messages to the chat terminal
function appendMessage(sender, text, isUser = false, type = "system") {
  const div = document.createElement("div");
  div.className = "sys-msg";

  const timeStr = new Date().toTimeString().slice(0, 8);
  
  let badgeClass = "system";
  if (sender === "ANVÄNDARE") badgeClass = "user";
  if (sender === "IGRIS") badgeClass = "agent";
  if (type === "success") badgeClass = "success";

  div.innerHTML = `
    <div class="sys-header">
      <span class="sys-badge ${badgeClass}">${sender}</span>
      <span class="sys-time">${timeStr}</span>
    </div>
    <div class="sys-body ${isUser ? "user-msg" : ""}">${text}</div>
  `;

  msgsContainer.appendChild(div);
  msgsContainer.scrollTop = msgsContainer.scrollHeight;
  return div.querySelector(".sys-body");
}

function logger(message) {
  console.log(`[system] ${message}`);
}

// Render active agent army
function updateAgents(agents) {
  const container = document.querySelector("#agentList");
  const countSpan = document.querySelector("#agentCount");
  
  countSpan.textContent = `${agents.length} online`;

  if (agents.length === 0) {
    container.innerHTML = `<div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text-dim);text-align:center;padding:10px 0;">Inga skuggagenter hittades</div>`;
    return;
  }

  container.innerHTML = agents.map(agent => {
    // S/A/B/Level 0 mapping based on rank
    let rankLabel = "B";
    if (agent.rank === "a_rank") rankLabel = "A";
    if (agent.rank === "b_rank") rankLabel = "B";
    if (agent.rank === "level_0") rankLabel = "L0";
    
    // Status color mapping
    let dotClass = "dot-idle";
    if (agent.status === "busy") dotClass = "dot-active";
    if (agent.status === "training") dotClass = "dot-training";
    if (agent.status === "error" || agent.status === "terminated") dotClass = "dot-blocked";

    const name = agent.name || agent.agent_id;
    const role = agent.language ? `${agent.language} worker` : "subagent";

    return `
      <div class="agent-row" title="Agent ID: ${agent.agent_id}">
        <div class="agent-rank ${agent.rank === "level_0" ? "level_0" : rankLabel}">${rankLabel}</div>
        <div class="agent-info">
          <div class="agent-name">${name}</div>
          <div class="agent-role">${role} (done: ${agent.tasks_completed})</div>
        </div>
        <div class="agent-status-dot ${dotClass}"></div>
      </div>
    `;
  }).join("");
}

// Render active tasks as Quest Items
function updateQuests(tasks) {
  const container = document.querySelector("#questList");
  const countSpan = document.querySelector("#questCount");

  const pendingQuests = tasks.filter(t => t.status === "pending" || t.status === "assigned" || t.status === "running");
  countSpan.textContent = `${pendingQuests.length} aktiva`;

  if (tasks.length === 0) {
    container.innerHTML = `<div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:var(--text-dim);text-align:center;padding:10px 0;">Inga aktiva uppdrag</div>`;
    return;
  }

  container.innerHTML = tasks.map(task => {
    let tag = "active";
    if (task.priority === "critical" || task.priority === "high") tag = "urgent";
    if (task.status === "completed") tag = "daily"; // use daily styling for finished quests

    const reward = task.priority === "critical" ? "+50 EXP" : task.priority === "high" ? "+25 EXP" : "+10 EXP";
    const statusLabel = task.status.toUpperCase();

    return `
      <div class="quest-item">
        <div class="quest-title">
          <span class="quest-tag ${tag}">${task.priority.toUpperCase()}</span>
          ${task.description.slice(0, 45)}${task.description.length > 45 ? "..." : ""}
        </div>
        <div class="quest-meta">Belöning: ${reward} · Status: ${statusLabel}</div>
      </div>
    `;
  }).join("");
}

// Poll GPU telemetry
async function pollGpu() {
  try {
    const response = await fetch("/gpu", { headers: getHeaders() });
    if (!response.ok) {
      if (response.status === 429) {
        logger("GPU telemetry requests rate-limited.");
      }
      return;
    }
    const data = await response.json();
    
    const snapshot = data.snapshot || { free_gb: 24.0, total_gb: 24.0, used_gb: 0.0, temperature_c: 0, utilization_pct: 0 };
    const oom = data.oom_risk || { risk: "low" };

    const total = snapshot.total_gb || 24.0;
    const used = snapshot.used_gb || 0.0;
    const free = snapshot.free_gb || 24.0;
    const usagePct = (used / total) * 100;

    // Update GPU Panel info
    document.querySelector("#vramText").textContent = `${used.toFixed(1)} / ${total.toFixed(1)} GB`;
    document.querySelector("#vramBar").style.width = `${usagePct}%`;
    document.querySelector("#gpuTemp").textContent = `${snapshot.temperature_c}°C`;
    document.querySelector("#gpuLoad").textContent = `${snapshot.utilization_pct}%`;
    
    // OOM Risk text & color
    const riskSpan = document.querySelector("#oomRisk");
    riskSpan.textContent = oom.risk.toUpperCase();
    if (oom.risk === "critical") riskSpan.style.color = "var(--red)";
    else if (oom.risk === "high") riskSpan.style.color = "var(--gold)";
    else riskSpan.style.color = "var(--green)";

    // Bind MP bar in topbar to VRAM free ratio
    const freePct = (free / total) * 100;
    document.querySelector("#mpFill").style.width = `${freePct}%`;

  } catch (error) {
    console.error("Failed to poll GPU telemetry:", error);
  }
}

// Send execution request to chat endpoint (streaming SSE)
async function sendCommand() {
  const text = chatIn.value.trim();
  if (!text) return;

  chatIn.value = "";
  // Append user prompt
  appendMessage("ANVÄNDARE", text, true);

  // Append empty placeholder for streaming response
  const responseBubble = appendMessage("IGRIS", "", false);

  try {
    const payload = {
      model: "qwen2.5-coder:32b",
      messages: [{ role: "user", content: text }],
      stream: true
    };

    const response = await fetch("/chat", {
      method: "POST",
      headers: getHeaders(),
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      if (response.status === 429) {
        responseBubble.innerHTML = `<span style="color:var(--red);">[ SYSTEM ERROR ] 429 Too Many Requests. Du skickar för många kommandon.</span>`;
      } else if (response.status === 502) {
        responseBubble.innerHTML = `<span style="color:var(--red);">[ SYSTEM ERROR ] 502 Bad Gateway. Ollama-motorn är offline.</span>`;
      } else {
        const errJson = await response.json().catch(() => ({ detail: "Okänt fel" }));
        responseBubble.innerHTML = `<span style="color:var(--red);">[ ERROR ] ${response.status}: ${errJson.detail || "Kunde inte slutföra order."}</span>`;
      }
      return;
    }

    // Read NDJSON stream from FastAPI
    const reader = response.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      
      // Save last unfinished chunk back to buffer
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.trim()) continue;
        try {
          const parsed = JSON.parse(line);
          // Parse standard Ollama message stream chunk
          if (parsed.message && parsed.message.content) {
            responseBubble.textContent += parsed.message.content;
            msgsContainer.scrollTop = msgsContainer.scrollHeight;
          }
          // Parse fallback error chunks
          if (parsed.error) {
            responseBubble.innerHTML += `<br><span style="color:var(--red);">[ ERROR ] ${parsed.error}</span>`;
          }
        } catch (e) {
          // Fallback to appending raw chunk if it's text
          responseBubble.textContent += line;
        }
      }
    }

    // Complete remaining buffer
    if (buffer.trim()) {
      try {
        const parsed = JSON.parse(buffer);
        if (parsed.message && parsed.message.content) {
          responseBubble.textContent += parsed.message.content;
        }
      } catch (e) {
        responseBubble.textContent += buffer;
      }
    }

  } catch (error) {
    console.error("Error in chat streaming:", error);
    responseBubble.innerHTML = `<span style="color:var(--red);">[ ANSLUTNINGSFEL ] Kunde inte kontakta servern. Kontrollera nätverket.</span>`;
  }
}

// Event Listeners
sendBtn.addEventListener("click", sendCommand);
chatIn.addEventListener("keydown", (e) => {
  if (e.key === "Enter") sendCommand();
});

saveToken.addEventListener("click", () => {
  const token = tokenInput.value.trim();
  if (token) {
    localStorage.setItem("igris-api-token", token);
    logger("Ny API-token sparad.");
    appendMessage("SYSTEM", "API-token uppdaterad. Återansluter...", false, "success");
    connectWebSocket();
    pollGpu();
  }
});

// Initialize on page load
tokenInput.value = getToken();
connectWebSocket();
pollGpu();
setInterval(pollGpu, 3000);
