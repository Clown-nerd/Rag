import React from "react";
import ChatWidget from "./ChatWidget";

export default function App() {
  return (
    <div className="app-root">
      <header className="app-header">Insurance Website Demo</header>
      <main className="app-main">
        <ChatWidget />
      </main>
    </div>
  );
}