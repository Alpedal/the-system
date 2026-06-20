const DEFAULT_TOKEN = "igris-dev-token";
const tokenInput = document.querySelector("#tokenInput");
const saveToken = document.querySelector("#saveToken");
const refreshBtn = document.querySelector("#refreshBtn");
const apiStatus = document.querySelector("#apiStatus");

const mockAgents = [
  { agent_id: "agent-python-001", status: "idle", rank: "b_rank" },
  { agent_id: "agent-review-002", status: "busy", rank: "a_rank" },
  { agent_id: "agent-security-003", status: "training", rank: "b_rank" },
  { agent_id: "agent-ui-004", status: "idle", rank: "level_0" },
  { agent_id: "agent-gpu-005", status: "idle", rank: "a_rank" },
  { agent_id: "agent-docs-006", status: "busy", rank: "b_rank" },
  { agent_id: "agent-test-007", status: "idle", rank: "b_rank" },
];

function getToken() {
  return localStorage.getItem("igris-api-token") || DEFAULT_TOKEN;
}

function setStatus(mode, text) {
  apiStatus.textContent = text;
  apiStatus.classList.toggle("offline", mode !== "online");
}

async function fetchJson(path) {
  const response = await fetch(path, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  if (!response.ok) throw new Error(`${path} returned ${response.status}`);
  return response.json();
}

function renderAgents(agents) {
  document.querySelector("#agentsOnline").textContent = String(agents.length).padStart(2, "0");
}

function renderGpu(gpu) {
  const snapshot = gpu.snapshot || { free_gb: 12.0 };
  const risk = gpu.oom_risk || { risk: "low" };
  document.querySelector("#vramFree").textContent = Number(snapshot.free_gb || 0).toFixed(1);
  document.querySelector("#oomText").textContent = `risk ${risk.risk}`;
}

async function refresh() {
  try {
    const [agents, gpu] = await Promise.all([fetchJson("/agents"), fetchJson("/gpu")]);
    renderAgents(agents);
    renderGpu(gpu);
    setStatus("online", "API online");
  } catch (error) {
    renderAgents(mockAgents);
    renderGpu({ snapshot: { free_gb: 12.0 }, oom_risk: { risk: "mock" } });
    setStatus("mock", "Mock mode");
  }
}

tokenInput.value = getToken();
saveToken.addEventListener("click", () => {
  localStorage.setItem("igris-api-token", tokenInput.value.trim() || DEFAULT_TOKEN);
  refresh();
});
refreshBtn.addEventListener("click", refresh);
refresh();
