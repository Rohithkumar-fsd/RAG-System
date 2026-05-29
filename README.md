# 🤖 RAG Chat System — Full Stack AI Document Q&A

A full-stack Retrieval-Augmented Generation (RAG) chatbot that combines Java, Python, and modern AI to answer questions based on stored documents using semantic search and LLMs.

## 🚀 Overview

This project implements a production-style RAG pipeline where user queries are processed through multiple microservices:

- ⚛️ **React frontend** collects user input
- ☕ **Spring Boot** acts as an API gateway
- 🐍 **Flask** runs the RAG engine
- 🗄️ **ChromaDB** retrieves relevant documents using embeddings
- 🧠 **Google Gemini** generates final answers

---

## 🏗️ Architecture
React UI (Port 5173)
↓
Spring Boot REST API (Port 8080)
↓
Flask RAG Service (Port 5000)
↓
LangChain + ChromaDB (Vector Search)
↓
Google Gemini LLM
↓
Response returned back to UI

---

## ⚙️ Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| React.js | UI Framework |
| Axios | HTTP Requests |
| CSS | Styling |

### Backend (Java)
| Technology | Purpose |
|---|---|
| Spring Boot | REST API Gateway |
| RestTemplate | Inter-service Communication |
| Maven | Dependency Management |

### Backend (Python RAG)
| Technology | Purpose |
|---|---|
| Flask | RAG Microservice |
| LangChain | RAG Pipeline |
| ChromaDB | Vector Database |
| Google Gemini | Embeddings + LLM |
| Python-dotenv | Environment Variables |

---

## ✨ Features

- 💬 Chat-based question answering system
- 📄 Retrieval-based document search (RAG)
- 🔍 Semantic similarity search using embeddings
- 🤖 AI-generated contextual responses
- 🌐 Full-stack microservice architecture
- ☕ Spring Boot as middleware API gateway
- ⚡ Real-time request handling across services

---

## 🧩 How It Works

User enters a question in React UI
↓
Request sent to Spring Boot (/ask)
↓
Spring Boot forwards to Flask (/chat)
↓
Flask Pipeline:
a. Converts query into embeddings
b. Searches ChromaDB for relevant chunks
c. Sends context + question to Gemini
↓
Gemini generates accurate response
↓
Response returned to frontend and displayed


---

## 📁 Project Structure
RAG-Chat-System/
│
├── rag-frontend/                  # React Frontend
│   ├── src/
│   │   ├── App.jsx                # Main chat component
│   │   └── App.css                # Styling
│   ├── package.json
│   └── vite.config.js
│
├── spring-backend/                # Java Spring Boot
│   ├── src/main/java/
│   │   └── RagController.java     # API Gateway Controller
│   └── pom.xml
│
├── flask-backend/                 # Python RAG Engine
│   ├── app.py                     # Flask API
│   ├── retrieval_pipeline.py      # RAG Pipeline
│   ├── ingestion_pipeline.py      # PDF Processing
│   └── requirements.txt
│
├── docs/                          # PDF Documents
│   └── *.pdf
│
├── db/                            # ChromaDB Vector Store
│   └── chroma_db/
│
├── .env                           # API Keys (not in repo)
├── .gitignore
└── README.md

---

## 🔧 Installation & Setup

### Prerequisites
- Java 17+
- Python 3.10+
- Node.js 18+
- Maven
- Google AI API Key

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Rohithkumar-fsd/RAG-System.git
cd RAG-System
```

---

### 2️⃣ Setup Python Backend (Flask + RAG)

```bash
cd flask-backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

Create `.env` file:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

Process documents:
```bash
python ingestion_pipeline.py
```

Run Flask server:
```bash
python app.py
```
Flask runs at: `http://127.0.0.1:5000`

---

### 3️⃣ Setup Spring Boot Backend

- Open project in **IntelliJ IDEA** or **Eclipse**
- Ensure Maven dependencies are installed

```bash
mvn spring-boot:run
```
Spring Boot runs at: `http://localhost:8080`

---

### 4️⃣ Setup React Frontend

```bash
cd rag-frontend
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173`

---

## 📡 API Endpoints

### Spring Boot API
**POST** `/ask`

Request:
```json
{
  "question": "Who founded Microsoft?"
}
```

Response:
```json
{
  "answer": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975."
}
```

---

### Flask RAG API
**POST** `/chat`

Request:
```json
{
  "question": "Where is Nvidia headquartered?"
}
```

Response:
```json
{
  "answer": "Nvidia is headquartered in Santa Clara, California, United States."
}
```

---

## 🔑 Getting Google API Key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **"Get API Key"**
3. Click **"Create API Key"**
4. Copy and paste into your `.env` file

---

## ⚠️ Known Issues

- Gemini API free-tier quota limits may cause rate limit errors
- Flask server **must be running** before starting Spring Boot
- Some Gemini model versions may become unavailable over time
- Ensure correct API keys are set in `.env` file

---

## 🔮 Future Improvements

- 🔥 Streaming responses (ChatGPT-style typing effect)
- 🔥 Upload custom documents dynamically via UI
- 🔥 Replace Flask with FastAPI for better performance
- 🔥 Add user authentication system
- 🔥 Deploy on cloud (AWS / GCP / Railway)
- 🔥 Support multiple document formats (Word, CSV, TXT)

---

## 📊 Why RAG over normal LLM?

| Feature | Normal LLM | RAG System |
|---|---|---|
| Knowledge source | Training data only | Your documents |
| Hallucination | High risk | Low risk |
| Up-to-date info | ❌ | ✅ |
| Source citations | ❌ | ✅ |
| Custom documents | ❌ | ✅ |

---

## 👨‍💻 Author

**Rohith Kumar**

## ⭐ If you found this project helpful, please give it a star!

> Built with ❤️ using React + Spring Boot + Flask + LangChain + Google Gemini
