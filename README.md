🚀 QueryWave
Intelligent Retrieval-Augmented AI Platform
🌊 Overview

QueryWave is a modular, end-to-end, industry-grade Retrieval-Augmented Generation (RAG) system built using fully open-source tools.

It enables users to:

📄 Upload documents and query them

🌐 Ask web-based questions

📚 Query arXiv research papers using paper IDs

🧠 Maintain chat memory with contextual awareness

⚡ Use hybrid search (Vector + BM25)

🤖 Generate grounded responses via Llama3 (Ollama)

This project was built with production-grade architecture principles in mind.

🎯 Core Features
1️⃣ Document Q&A

Upload PDF, DOCX, TXT

Automatic chunking

Hybrid retrieval (Vector + BM25)

Context-grounded LLM answers

Source citation display

2️⃣ Web Search Mode

Real-time retrieval

Query routing

Context injection into LLM

3️⃣ arXiv Paper Q&A

Enter arXiv paper ID

Download PDF dynamically

Build temporary vector index

Ask questions grounded in the paper

4️⃣ Chat Memory

Conversation stored in session

Relevance filtering

Context-aware response generation

5️⃣ Premium UI

Cinematic neural background

Floating particle animation

Glassmorphism design

History toggle panel

Fully interactive sidebar

🏗 System Architecture

QueryWave follows a layered architecture:

User Interface (Streamlit)
        ↓
Router Layer
        ↓
Tool Manager
        ↓
Pipeline Layer (Document / Web / arXiv)
        ↓
Hybrid Retriever
        ↓
Context Builder
        ↓
LLM (Llama3 via Ollama)
        ↓
Response Generator

🧠 Execution Flow
Step 1: Mode Selection

User selects:

Document

Web

arXiv

The selected mode is stored in session state.

Step 2: Query Routing
route_query(user_query, state)


The router determines which pipeline should handle the request.

Step 3: Tool Execution
execute_tool(routing_payload)


Tool Manager triggers:

_execute_document_pipeline

_execute_web_pipeline

_execute_arxiv_pipeline

Step 4: Retrieval

Document & arXiv modes use:

HuggingFace Embeddings (all-MiniLM-L6-v2)

FAISS Vector Store

BM25 keyword search

Hybrid scoring

Step 5: Context Building

The system builds structured context:

Retrieved chunks

Filtered chat history

User query

This ensures grounded generation.

Step 6: LLM Response
OllamaLLM.generate(prompt)


Llama3

Retry logic

Timeout handling

Structured error handling

Step 7: Response Rendering

Assistant response

Source citations

Stored in chat memory

📂 Project Structure
QueryWave/
│
├── app/
│   ├── orchestration/
│   │   ├── router.py
│   │   ├── tool_manager.py
│   │   └── context_builder.py
│   │
│   ├── pipelines/
│   │   ├── document_rag/
│   │   ├── arxiv_rag/
│   │   └── web_rag/
│   │
│   ├── memory/
│   │   ├── chat_history.py
│   │   └── relevance_filter.py
│   │
│   ├── llm/
│   │   ├── model_loader.py
│   │   ├── embeddings.py
│   │   └── response_generator.py
│   │
│   └── utils/
│
├── app2.py
├── background.png
└── README.md

🛠 Technology Stack
Layer	Technology
UI	Streamlit
LLM	Llama3 (Ollama)
Embeddings	sentence-transformers
Vector Store	FAISS
Keyword Search	BM25
PDF Parsing	PyMuPDF
arXiv API	arxiv Python package
Logging	Custom Logger
Error Handling	Custom Exceptions
🔐 Engineering Decisions
✔ Modular Architecture

Each responsibility is isolated:

Routing

Execution

Retrieval

LLM

Memory

✔ Hybrid Retrieval

Combines:

Semantic similarity

Keyword relevance

Improves factual grounding.

✔ Fault Tolerance

Retry decorator

Timeout protection

Structured exceptions

✔ Session-Based Caching

Document retriever cached

arXiv retriever cached

Reduces repeated indexing

🚀 How to Run
1️⃣ Install dependencies
pip install -r requirements.txt

2️⃣ Start Ollama
ollama run llama3

3️⃣ Launch app
streamlit run app2.py

🎥 Demo Capabilities

Upload a resume → ask skill-related questions

Enter 1706.03762 → ask about Transformers paper

Switch to Web mode → general knowledge queries

Toggle history panel

View retrieved source chunks

📈 What This Project Demonstrates

End-to-end RAG system design

LLM integration

Hybrid retrieval engineering

API integration (arXiv)

State management

Fault-tolerant architecture

Production-style modularization

UI/UX engineering

System-level thinking

🔮 Future Enhancements

Persistent vector database (Chroma)

Multi-user authentication

Token budget control

Streaming token animation

Deployment (Docker / Cloud)

Evaluation metrics dashboard

🏆 Portfolio Impact

QueryWave is not a tutorial implementation.

It is:

A structured RAG system

With hybrid retrieval

Dynamic arXiv indexing

Production-grade architecture

Premium user interface