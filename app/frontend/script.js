const API_BASE = "http://127.0.0.1:8000";

const fileInput = document.getElementById("fileInput");
const statusText = document.getElementById("statusText");
const jsonBox = document.getElementById("jsonBox");
const hashInput = document.getElementById("hashInput");
const btnCopyHash = document.getElementById("btnCopyHash");
const resultBadge = document.getElementById("resultBadge");
btnCopyHash.addEventListener("click", async () => {
  const hash = (hashInput.value || "").trim();

  if (!hash) {
    setStatus("Não há hash para copiar.", true);
    return;
  }

  await navigator.clipboard.writeText(hash);
  setStatus("Hash copiado ✅", false);
});
const btnUpload = document.getElementById("btnUpload");
const btnCheck = document.getElementById("btnCheck");

document.getElementById("year").innerText = new Date().getFullYear();

btnUpload.addEventListener("click", uploadFile);
btnCheck.addEventListener("click", verifyHash);

function setStatus(text, isError = false) {
  statusText.textContent = text;
  statusText.style.color = isError ? "rgba(255,120,120,.95)" : "var(--cyan)";
}

function setJson(data) {
  jsonBox.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
}

async function uploadFile() {
  if (!fileInput.files.length) {
    setStatus("Selecione um arquivo primeiro.", true);
    setJson("");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]); // ✅ seu swagger mostra que o campo é "file"

  setStatus("Registrando arquivo...", false);
  setJson("");

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      body: formData,
    });

    const data = await res.json();

    if (!res.ok) {
      setStatus("Falha ao registrar (ver resposta).", true);
      setJson(data);
      return;
    }

    const hash = data?.certificate?.sha256; // ✅ retorno real do seu backend
    if (hash) hashInput.value = hash;

    setStatus("Registrado ✅ Hash gerado.", false);
    setJson(data);
  } catch (err) {
    setStatus("Erro ao conectar com a API.", true);
    setJson(String(err));
  }
}

async function verifyHash() {
  const hash = (hashInput.value || "").trim();

  if (!hash) {
    setStatus("Cole um hash para verificar.", true);
    setJson("");
    return;
  }

  setStatus("Verificando hash...", false);
  setJson("");

  try {
    const res = await fetch(`${API_BASE}/verify/${encodeURIComponent(hash)}`, {
      method: "GET",
    });

    const data = await res.json();

    if (!res.ok) {
      setStatus("Falha na verificação (ver resposta).", true);
      setJson(data);
      return;
    }

    setStatus("Verificação concluída ✅", false);
    setJson(data);
  } catch (err) {
    setStatus("Erro ao conectar com a API.", true);
    setJson(String(err));
  }
}