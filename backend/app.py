# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from chatbot.rag_pipeline import RAGPipeline
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app, origins=["https://gov-chatbot-bfe73.web.app"])

# Initialize RAG pipeline
print("Initializing Samarth backend...")
rag_pipeline = RAGPipeline()

# Check if data needs to be indexed
if not rag_pipeline.is_indexed:
    print("Vector store not found. Indexing data...")
    # In production, you might want to do this asynchronously
    # For now, we'll do it at startup
    try:
        rag_pipeline.index_data()
    except Exception as e:
        print(f"Error during indexing: {e}")
        print("Continuing without indexed data. Some features may not work.")

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'Project Samarth - Agricultural Data Q&A System',
        'version': '1.0.0',
        'indexed': rag_pipeline.is_indexed,
        'vector_store_stats': rag_pipeline.vector_store.get_stats()
    })

@app.route('/api/query', methods=['POST'])
def query():
    """
    Main query endpoint
    
    Request JSON:
        {
            "query": "User's question",
            "num_sources": 5  # Optional, default 5
        }
    
    Response JSON:
        {
            "answer": "Generated answer",
            "sources": [...],
            "query_info": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        
        user_query = data['query']
        
        # Process query through RAG pipeline
        result = rag_pipeline.answer_query(user_query)
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/index', methods=['POST'])
def index_data():
    """
    Endpoint to trigger data indexing
    
    This should be called when you want to refresh the data
    """
    try:
        rag_pipeline.index_data()
        return jsonify({
            'status': 'success',
            'message': 'Data indexed successfully',
            'stats': rag_pipeline.vector_store.get_stats()
        })
    except Exception as e:
        print(f"Error indexing data: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    return jsonify({
        'vector_store': rag_pipeline.vector_store.get_stats(),
        'cache': rag_pipeline.cache_manager.get_stats(),
        'is_indexed': rag_pipeline.is_indexed
    })

@app.route('/api/search_datasets', methods=['POST'])
def search_datasets():
    """Search for datasets on data.gov.in"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        results = rag_pipeline.data_client.search_resources(query)
        
        return jsonify({
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = Config.FLASK_PORT
    debug = Config.DEBUG
    
    print(f"\n{'='*60}")
    print(f"Starting Project Samarth Backend Server")
    print(f"{'='*60}")
    print(f"Port: {port}")
    print(f"Debug Mode: {debug}")
    print(f"Vector Store Indexed: {rag_pipeline.is_indexed}")
    print(f"{'='*60}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)