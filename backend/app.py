from flask import Flask, request, jsonify
from flask_cors import CORS
from config import Config
from chatbot.rag_pipeline import RAGPipeline
import os
import threading
import logging

# Configure structured logging for Cloud Run
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://gov-chatbot-bfe73.web.app"]}})

# Initialize RAG pipeline
print("Initializing Samarth backend...")
rag_pipeline = RAGPipeline()

# --- Async data indexing function ---
def start_indexing_async():
    try:
        rag_pipeline.index_data()
    except Exception as e:
        print(f"Error during background indexing: {e}")

# --- Startup indexing if needed, in background ---
if not rag_pipeline.is_indexed:
    print("Vector store not found. Indexing data in background...")
    thread = threading.Thread(target=start_indexing_async, daemon=True)
    thread.start()

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
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({'error': 'No query provided'}), 400
        user_query = data['query']
        result = rag_pipeline.answer_query(user_query)
        return jsonify(result)
    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/index', methods=['POST'])
def index_data():
    """
    Endpoint to trigger data indexing asynchronously
    """
    if rag_pipeline.is_indexed:
        return jsonify({
            'status': 'done',
            'message': 'Already indexed',
            'stats': rag_pipeline.vector_store.get_stats()
        })
    else:
        # Start background thread to index data
        thread = threading.Thread(target=start_indexing_async, daemon=True)
        thread.start()
        return jsonify({
            'status': 'indexing',
            'message': 'Indexing started, check /api/stats for progress'
        }), 202

@app.route('/api/stats', methods=['GET'])
def get_stats():
    vector_stats = {}
    cache_stats = {}
    try:
        if hasattr(rag_pipeline, "vector_store"):
            vector_stats = rag_pipeline.vector_store.get_stats()
        if hasattr(rag_pipeline, "cache_manager"):
            cache_stats = rag_pipeline.cache_manager.get_stats()
    except Exception as e:
        logger.warning(f"Error retrieving stats: {e}")

    return jsonify({
        'vector_store': vector_stats,
        'cache': cache_stats,
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
