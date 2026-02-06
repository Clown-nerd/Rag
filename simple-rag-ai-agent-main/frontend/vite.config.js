import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // During development proxy /chat, /draft, /ingest, /upload, /settings to the backend
    proxy: {
      "/chat": "http://localhost:8000",
      "/draft": "http://localhost:8000",
      "/ingest": "http://localhost:8000",
      "/upload": "http://localhost:8000",
      "/settings": "http://localhost:8000",
    },
  },
});
