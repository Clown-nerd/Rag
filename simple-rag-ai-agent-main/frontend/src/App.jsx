import React from "react";
import ChatWidget from "./ChatWidget";

export default function App() {
  return (
    <div className="app-root">
      <header className="app-header">Kenya Law Firm – Legal Assistant</header>
      <main className="app-main">
        <ChatWidget />
      </main>
    </div>
  );
}