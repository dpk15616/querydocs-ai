# QueryDocs AI – Context-Aware Document QA using RAG

## Overview
QueryDocs AI is a Retrieval-Augmented Generation (RAG) system that allows users to upload documents and query them using natural language. It combines semantic retrieval with LLM-based response generation to provide accurate, context-aware answers.

## Features
- Upload and process PDF documents
- Semantic chunking and embeddings
- Vector similarity search (FAISS)
- Context-aware answer generation using Groq LLM
- REST API using FastAPI
- Streamlit UI for interaction
- Docker support

## Architecture
User → Streamlit UI → FastAPI Backend → RAG Pipeline  
RAG Pipeline = Ingestion → Embedding → Vector DB → Retrieval → LLM Response

## Tech Stack
- **Backend:** Python, FastAPI
- **Frontend:** Streamlit
- **RAG Framework:** LangChain
- **Vector DB:** FAISS (local)
- **Embeddings:** HuggingFace Sentence Transformers (free, runs locally)
- **LLM:** Groq (llama-3.3-70b-versatile)

## Setup

### 1. Clone repo
```bash
git clone https://github.com/your-username/querydocs-ai.git
cd querydocs-ai
```

### 2. Create virtual environment
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your **Groq API key**:
- Get free API key from [Groq Console](https://console.groq.com/keys)
- **Note:** OpenAI API key is NOT required (using free HuggingFace embeddings)

### 5. Run backend
```bash
uvicorn app.main:app --reload
```
Backend will run on `http://localhost:8000`

### 6. Run UI (in new terminal)
```bash
source env/bin/activate
streamlit run ui/streamlit_app.py
```
UI will run on `http://localhost:8501`

## Docker
```
docker build -t querydocs-ai .
docker run -p 8000:8000 querydocs-ai
```

## Future Improvements
- Add Pinecone / Weaviate support
- Add reranking for better retrieval
- Add evaluation metrics
- Add caching layer (Redis)
- Add authentication

## Author
Deepak Gupta
