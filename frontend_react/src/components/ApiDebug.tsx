import React, { useState } from "react";
import { movieService } from "../services/api";

const ApiDebug: React.FC = () => {
  const [logs, setLogs] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const addLog = (message: string) => {
    setLogs((prev) => [
      ...prev,
      `${new Date().toLocaleTimeString()}: ${message}`,
    ]);
  };

  const testApi = async () => {
    setLoading(true);
    addLog("Starting API test...");

    try {
      // Test 1: Simple API call
      addLog("Testing simple API call to /movies/");
      const response = await fetch("http://localhost:8000/movies/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });

      addLog(`Response status: ${response.status}`);
      addLog(
        `Response headers: ${JSON.stringify(Object.fromEntries(response.headers.entries()))}`,
      );

      const contentType = response.headers.get("content-type");
      addLog(`Content-Type: ${contentType}`);

      if (!response.ok) {
        const errorText = await response.text();
        addLog(`Error response: ${errorText}`);
        return;
      }

      const data = await response.text();
      addLog(`Response data length: ${data.length} characters`);
      addLog(`First 200 chars of response: ${data.substring(0, 200)}...`);

      // Test 2: Using our movie service
      addLog("Testing movieService.fetchMovies...");
      const movies = await movieService.fetchMovies({ limit: 5 });
      addLog(`Successfully fetched ${movies.length} movies`);
      if (movies.length > 0) {
        addLog(`First movie title: ${movies[0]?.title || "N/A"}`);
      }
    } catch (error) {
      addLog(`Error: ${error}`);
    } finally {
      setLoading(false);
    }
  };

  const clearLogs = () => {
    setLogs([]);
  };

  return (
    <div style={{ padding: "20px", fontFamily: "monospace" }}>
      <h2>API Debug Tool</h2>
      <div style={{ marginBottom: "20px" }}>
        <button
          onClick={testApi}
          disabled={loading}
          style={{ marginRight: "10px" }}
        >
          {loading ? "Testing..." : "Test API"}
        </button>
        <button onClick={clearLogs}>Clear Logs</button>
      </div>
      <div
        style={{
          background: "#1a1a1a",
          color: "#00ff00",
          padding: "10px",
          borderRadius: "4px",
          height: "300px",
          overflowY: "auto",
          whiteSpace: "pre-wrap",
          fontSize: "12px",
        }}
      >
        {logs.length === 0
          ? 'Click "Test API" to begin debugging...'
          : logs.join("\n")}
      </div>
    </div>
  );
};

export default ApiDebug;
