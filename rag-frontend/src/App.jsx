import { useState } from "react";

import axios from "axios";

import "./App.css";

function App()
{
  const[question,setQuestion]=useState("");
  const[messages,setmessages]=useState([]);
  const[loading,setloading]=useState(false);
  
  const sendQuestion=async()=>{
     if(!question.trim()) 
     {
      return;
     }
     const userMessage={
      sender:"user",
      text:question
     };
     setmessages(prev => [...prev, userMessage]);
     setloading(true);
     try{
        const response=await axios.post("http://localhost:8080/ask",
        {
          question:question
        });
        console.log(response.data);
        const botmessage={
          sender:"bot",
          text:response.data.answer
        };
        setmessages((prev)=>[...prev,botmessage]);
     } 

     catch(error)
      {
        const erroemessage={
          sender:"bot",
          text:"Error connecting to server"
        };
        setmessages((prev)=>[...prev,erroemessage]);
      }
      setQuestion("");
      setloading(false);
   };
   return (
    <div className="container">

      <div className="chat-box">

        <h1>RAG Chat Assistant</h1>

        <div className="messages">

          {messages.map((msg, index) => (
            <div
              key={index}
              className={
                msg.sender === "user"
                  ? "message user"
                  : "message bot"
              }
            >
              {msg.text}
            </div>
          ))}

          {loading && (
            <div className="message bot">
              Thinking...
            </div>
          )}

        </div>

        <div className="input-area">

          <input
            type="text"
            placeholder="Ask something..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendQuestion();
              }
            }}
          />

          <button onClick={sendQuestion}>
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

export default App;