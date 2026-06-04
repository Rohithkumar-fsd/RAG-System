import { useState, useRef, useEffect } from "react";
import axios from "axios";
import "./App.css";

const SUGGESTIONS = ["Summarize key findings", "What are the risks?", "Show action items"];

export default function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi! Ask me anything about your documents — I'll find the most relevant answers." }
  ]);
  const [loading, setLoading] = useState(false);
  const msgsRef = useRef(null);

  useEffect(() => {
    if (msgsRef.current)
      msgsRef.current.scrollTop = msgsRef.current.scrollHeight;
  }, [messages, loading]);

  const sendQuestion = async (text) => {
    const q = (text ?? question).trim();
    if (!q) return;
    setMessages(prev => [...prev, { sender: "user", text: q }]);
    setQuestion("");
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8080/ask", { question: q });
      setMessages(prev => [...prev, { sender: "bot", text: res.data.answer }]);
    } catch {
      setMessages(prev => [...prev, { sender: "bot", text: "Error connecting to server." }]);
    }
    setLoading(false);
  };

  return (
    <div className="chat-wrapper">
      <div className="chat-card">

        <div className="chat-header">
          <div className="header-logo">
            <i className="ti ti-brain" />
          </div>
          <div className="header-info">
            <h2>RAG Assistant</h2>
            <p>Powered by your documents</p>
          </div>
          <div className="online-dot" title="Online" />
        </div>

        <div className="messages" ref={msgsRef}>
          {messages.map((msg, i) => (
            <div key={i} className={`msg-row ${msg.sender === "user" ? "user" : ""}`}>
              <div className={`avatar ${msg.sender}`}>
                <i className={`ti ${msg.sender === "user" ? "ti-user" : "ti-brain"}`} />
              </div>
              <div className={`bubble ${msg.sender}`}>{msg.text}</div>
            </div>
          ))}
          {loading && (
            <div className="msg-row">
              <div className="avatar bot"><i className="ti ti-brain" /></div>
              <div className="bubble bot">
                <span className="thinking-dots">
                  <span /><span /><span />
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="suggestions">
          {SUGGESTIONS.map(s => (
            <button key={s} className="chip" onClick={() => sendQuestion(s)}>{s}</button>
          ))}
        </div>

        <div className="input-area">
          <input
            type="text"
            placeholder="Ask something about your documents…"
            value={question}
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => e.key === "Enter" && sendQuestion()}
          />
          <button className="send-btn" onClick={() => sendQuestion()} aria-label="Send">
            <i className="ti ti-send" />
          </button>
        </div>

      </div>
    </div>
  );
}
