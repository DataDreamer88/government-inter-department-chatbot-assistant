# Project Samarth - Complete Code Implementation

## Table of Contents
1. [Project Structure](#project-structure)
2. [Backend Code](#backend-code)
3. [Frontend Code](#frontend-code)
4. [Setup Instructions](#setup-instructions)
5. [Deployment Guide](#deployment-guide)

---

## Project Structure

```
project-samarth/
│
├── backend/
│   ├── app.py                          # Flask backend server
│   ├── config.py                       # Configuration settings
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example                    # Environment variables template
│   │
│   ├── data_fetcher/
│   │   ├── __init__.py
│   │   ├── data_gov_client.py         # data.gov.in API client
│   │   ├── data_processor.py          # Data cleaning and processing
│   │   └── cache_manager.py           # Caching layer
│   │
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── embedding_generator.py     # Generate embeddings
│   │   └── vector_store.py            # FAISS vector storage
│   │
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── llm_handler.py             # LLM integration
│   │   ├── rag_pipeline.py            # RAG implementation
│   │   └── query_processor.py         # Query processing
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py                  # Utility functions
│
├── frontend/
│   ├── package.json
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.js
│       ├── index.js
│       ├── App.css
│       └── components/
│           ├── ChatInterface.js
│           ├── MessageList.js
│           ├── InputBox.js
│           ├── Statistics.js
│           └── SourceCitation.js
│
└── notebooks/
    ├── data_exploration.ipynb
    └── rag_testing.ipynb
```

---

## Backend Code

### 1. backend/requirements.txt
```txt
flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
requests==2.31.0
pandas==2.1.4
numpy==1.26.2

# LLM and Embeddings
langchain==0.1.0
langchain-community==0.0.10
openai==1.6.1
groq==0.4.1
sentence-transformers==2.2.2

# Vector Store
faiss-cpu==1.7.4
chromadb==0.4.22

# API and Data Processing
cachetools==5.3.2
aiohttp==3.9.1
```

### 2. backend/.env.example
```env
# API Keys
DATA_GOV_API_KEY=your_data_gov_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
GROQ_API_KEY=your_groq_api_key_here

# Application Settings
FLASK_ENV=development
FLASK_PORT=5000
DEBUG=True

# LLM Configuration
LLM_PROVIDER=groq
LLM_MODEL=mixtral-8x7b-32768
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Cache Settings
CACHE_DURATION=3600
```

### 3. backend/config.py
```python

```

### 4. backend/data_fetcher/__init__.py
```python

```

### 5. backend/data_fetcher/data_gov_client.py
```python

```

### 6. backend/data_fetcher/data_processor.py
```python

```

### 7. backend/data_fetcher/cache_manager.py
```python

```

### 8. backend/embeddings/__init__.py
```python

```

### 9. backend/embeddings/embedding_generator.py
```python

```

### 10. backend/embeddings/vector_store.py
```python

```

---

## Continued in Part 2...

(Due to length constraints, the complete code will be provided in multiple parts. This includes Flask app, LLM handler, RAG pipeline, React frontend, setup instructions, and deployment guide.)
