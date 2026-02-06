import React, { useState } from "react";

export default function ChatWidget() {
  const [msgs, setMsgs] = useState([{ role: "bot", text: "Habari! I'm your legal assistant. Ask me about Kenyan law or request a document draft." }]);
  const [text, setText] = useState("");
  const [mode, setMode] = useState("chat"); // "chat" or "draft"

  async function send() {
    const msg = text.trim();
    if (!msg) return;

    setMsgs((m) => [...m, { role: "user", text: msg }]);
    setText("");

    const endpoint = mode === "draft" ? "http://localhost:8000/draft" : "http://localhost:8000/chat";
    const bodyKey = mode === "draft" ? "instruction" : "message";

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ [bodyKey]: msg }),
      });
      const data = await res.json();
      const reply = data.answer || data.draft;
      setMsgs((m) => [...m, { role: "bot", text: reply }]);
    } catch (err) {
      setMsgs((m) => [...m, { role: "bot", text: "Error contacting server." }]);
    }
  }

  return (
    <div className="chat-widget">
      <div className="mode-toggle">
        <button className={mode === "chat" ? "mode-btn active" : "mode-btn"} onClick={() => setMode("chat")}>Ask</button>
        <button className={mode === "draft" ? "mode-btn active" : "mode-btn"} onClick={() => setMode("draft")}>Draft</button>
      </div>

      <div className="messages" role="log" aria-live="polite">
        {msgs.map((m, i) => (
          <div key={i} className={"msg " + (m.role === "user" ? "msg-user" : "msg-bot") }>
            <div className="msg-text">{m.text}</div>
          </div>
        ))}
      </div>

      <div className="input-row">
        <input
          className="chat-input"
          placeholder={mode === "draft" ? "Describe the document to draft..." : "Ask a legal question..."}
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter") send(); }}
        />
        <button className="chat-send" onClick={send}>Send</button>
      </div>
    </div>
  );
}