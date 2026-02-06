import React, { useState, useEffect, useRef } from "react";
import ChatWidget from "./ChatWidget";

const API_BASE = window.location.origin;

function Sidebar({ activeTab, setActiveTab }) {
  const tabs = [
    { id: "chat", label: "💬 Assistant" },
    { id: "upload", label: "📄 Upload PDF" },
    { id: "settings", label: "⚙️ Settings" },
  ];
  return (
    <nav className="sidebar">
      <div className="sidebar-brand">⚖️ Kenya Law Firm</div>
      <div className="sidebar-subtitle">Legal AI Assistant</div>
      {tabs.map((t) => (
        <button
          key={t.id}
          className={"sidebar-tab" + (activeTab === t.id ? " active" : "")}
          onClick={() => setActiveTab(t.id)}
        >
          {t.label}
        </button>
      ))}
      <div className="sidebar-footer">
        Accessible to all computers on<br/>your office network
      </div>
    </nav>
  );
}

function UploadPanel() {
  const [status, setStatus] = useState(null);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef();

  async function handleUpload() {
    const file = fileRef.current?.files?.[0];
    if (!file) return;
    setUploading(true);
    setStatus(null);
    const form = new FormData();
    form.append("file", file);
    try {
      const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
      const data = await res.json();
      if (data.status === "ok") {
        setStatus(`✅ Uploaded "${data.file}" — ${data.chunks} chunks indexed.`);
      } else {
        setStatus(`❌ ${data.detail || "Upload failed."}`);
      }
    } catch {
      setStatus("❌ Could not reach the server.");
    } finally {
      setUploading(false);
    }
  }

  async function handleIngest() {
    setUploading(true);
    setStatus(null);
    try {
      const res = await fetch(`${API_BASE}/ingest`, { method: "POST" });
      const data = await res.json();
      setStatus(`✅ Ingested — ${data.chunks} chunks indexed.`);
    } catch {
      setStatus("❌ Could not reach the server.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div className="panel">
      <h2>Upload a PDF to the Knowledge Base</h2>
      <p className="panel-hint">
        Upload statutes, case law, contracts, or any legal PDF.
        It will be indexed immediately so the assistant can reference it.
      </p>
      <div className="upload-row">
        <input ref={fileRef} type="file" accept=".pdf" className="file-input" />
        <button className="btn" onClick={handleUpload} disabled={uploading}>
          {uploading ? "Uploading…" : "Upload & Index"}
        </button>
      </div>
      <hr className="divider" />
      <p className="panel-hint">Or re-index the default knowledge base PDF:</p>
      <button className="btn btn-secondary" onClick={handleIngest} disabled={uploading}>
        Re-index default PDF
      </button>
      {status && <div className="upload-status">{status}</div>}
    </div>
  );
}

function SettingsPanel() {
  const [cfg, setCfg] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/settings`)
      .then((r) => r.json())
      .then(setCfg)
      .catch(() => setCfg({ error: true }));
  }, []);

  if (!cfg) return <div className="panel"><p>Loading settings…</p></div>;
  if (cfg.error) return <div className="panel"><p>Could not load settings from server.</p></div>;

  return (
    <div className="panel">
      <h2>Current Configuration</h2>
      <p className="panel-hint">
        These values are set via environment variables in <code>backend/.env</code>. 
        Restart the server after changing them.
      </p>
      <table className="settings-table">
        <tbody>
          <tr><td className="settings-key">Ollama URL</td><td>{cfg.ollama_base_url}</td></tr>
          <tr><td className="settings-key">Chat Model</td><td>{cfg.chat_model}</td></tr>
          <tr><td className="settings-key">Embedding Model</td><td>{cfg.embed_model}</td></tr>
          <tr><td className="settings-key">Retrieval K</td><td>{cfg.retrieval_k}</td></tr>
        </tbody>
      </table>
      <hr className="divider" />
      <h3>Network Access</h3>
      <p className="panel-hint">
        Other computers on your network can access this assistant at:
      </p>
      <code className="network-url">{window.location.origin}</code>
      <p className="panel-hint" style={{marginTop: 8}}>
        Share this URL with other advocates in your office.
      </p>
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState("chat");

  return (
    <div className="app-layout">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="app-content">
        <header className="app-header">Kenya Law Firm – Legal Assistant</header>
        <main className="app-main">
          {activeTab === "chat" && <ChatWidget />}
          {activeTab === "upload" && <UploadPanel />}
          {activeTab === "settings" && <SettingsPanel />}
        </main>
      </div>
    </div>
  );
}