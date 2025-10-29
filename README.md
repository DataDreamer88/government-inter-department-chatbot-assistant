# Project Samarth – Intelligent Agricultural Q&A System

A full-stack AI system for natural language Q&A on Indian agricultural and climate datasets, built using Retrieval-Augmented Generation (RAG) principles, vector search, and LLM-driven reasoning over live data from [data.gov.in](https://data.gov.in/).

---

## 🚀 Project Overview

**Project Samarth** enables users to analyze India's agricultural economy and climate patterns by querying rainfall and crop production statistics in plain English. Leveraging open government APIs, machine learning embeddings, and LLMs, it delivers contextual answers and insights for researchers, policy makers, farmers, and students.

---

# Project Samarth - Explanation Video

Click the image below to watch the detailed explanation video for Project Samarth:
[![Watch Explanation Video]](https://drive.google.com/file/d/14hQsatp06XE5e80OlS1NtmesGnResFG4/view?usp=sharing)
<img width="1326" height="828" alt="image" src="<img width="1919" height="980" alt="Screenshot 2025-10-30 014607" src="https://github.com/user-attachments/assets/7e67ffe5-39ce-417b-ad4b-363d4419082e" />
" />

## 🛠 Technologies & Skills Used

- **Frontend:** React.js, HTML/CSS, JavaScript
- **Backend:** Python 3.11+, Flask, RESTful APIs, pandas, requests, python-dotenv
- **Machine Learning & AI:** SentenceTransformers (`all-MiniLM-L6-v2`), HuggingFace, Groq Llama-3.3-70b (via Groq API)
- **Retrieval & Storage:** Chroma Vector Store, LangChain patterns (custom RAG pipeline)
- **APIs:**  
  - [data.gov.in API](https://data.gov.in/) (crop & rainfall data)
  - [Groq LLM API](https://groq.com/) (for answer generation)
- **DevOps:** Docker, Python Virtual Environments, Google Cloud Run (backend deployment), Firebase Hosting (frontend hosting)
- **Other:** Environment variable management via `.env`, CORS setup for frontend-backend integration

---

## 🎯 Key Features

- **Live Data Ingestion:**  
  Dynamic fetching of agricultural and weather datasets from [data.gov.in] using robust REST API wrappers and filter support for states, crops, years, and districts.

- **Semantic Vector Search:**  
  Uses SentenceTransformer embeddings and Chroma vector store for efficient similarity search over thousands of records.

- **RAG Pipeline & LLM Response:**  
  Modular pipeline with:  
  - Retrieval (top-matching documents via vector search)  
  - Prompt construction and contextual grounding  
  - Language model (Groq Llama) for final answer formulation

- **Interactive Chat Frontend:**  
  User-friendly React UI with chat experience, sample queries, real-time feedback, and production-level API integration.

---

## 💡 Optimizations & Rationale

- **RAG Architecture:**  
  Enables reliable factual answers by combining retrieved data context with generative LLM reasoning.

- **Efficient Embedding & Indexing:**  
  Batch processing for vectorization, persistent Chroma store, and parametric filters empower fast data updates and scalable search.

- **Environment Isolation:**  
  Virtualenv, `.env` config, and strict requirements.txt for easy deployment and reproducibility.

- **Cloud-native Design:**  
  Deployed with Google Cloud Run (backend Dockerized API), scalable and network-accessible; Firebase used for global low-latency static frontend hosting.

- **Debug & Observability:**  
  Print/log coverage of states, crops, years (on startup), and sample data for transparent query/text tuning.

- **Why These Choices:**  
  - **Flask**: Simple, scalable web API, easy Python integration.  
  - **Chroma Vector Store**: Fast semantic retrieval, fits agricultural data scale.  
  - **SentenceTransformers**: Resource-efficient embeddings, proven QnA quality.  
  - **LangChain Pattern**: Flexible RAG composition even with custom code.  
  - **Groq LLM**: Production-grade generative answers, seamless API workflow.

---

## 🧑‍💻 Setup Guide

### 1. Clone the Repo & Configure Environment

```
git clone https://github.com/your-user/project-samarth.git
cd project-samarth/backend
python -m venv venv
source venv/Scripts/activate # (or source venv/bin/activate on Linux/Mac)
pip install -r requirements.txt
```
- Create a `.env` file in `/backend` with:
```
DATA_GOV_API_KEY=your_data_gov_api_key
GROQ_API_KEY=your_groq_api_key
```
### 2. Start the Backend Server
```
python app.py
```
Server will run on http://127.0.0.1:5000


### 3. Launch the Frontend
```
cd ../frontend
npm install
Set API URL in .env: REACT_APP_API_URL=http://127.0.0.1:5000
npm start
```
Visit [http://localhost:3000](http://localhost:3000).

### 4. Run in Production

- Deploy backend on Google Cloud Run (Dockerized build, HTTPS endpoint)
- Deploy frontend on Firebase Hosting (public domain)
- Set production backend endpoint in `REACT_APP_API_URL`

---

## 🔎 Usage Examples

- "Compare average annual rainfall in Punjab and Haryana for the last 5 years"
- "What is the top crop by production volume in Maharashtra?"
- "Analyze rainfall-crop correlation in Karnataka"

Supports flexible factual, comparative, and trend queries.

---

## 🔏 License

MIT License.  
See [LICENSE](LICENSE) for full details.

---

## 🙏 Credits

- Government of India – [data.gov.in](https://data.gov.in/)
- HuggingFace, ChromaDB, LangChain Community
- Groq, Google Cloud, Firebase

---





