
# Create comprehensive backend code files

# 1. Backend requirements.txt
backend_requirements = """# backend/requirements.txt
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
"""

print("="*80)
print("FILE: backend/requirements.txt")
print("="*80)
print(backend_requirements)

with open('/tmp/requirements.txt', 'w') as f:
    f.write(backend_requirements)
