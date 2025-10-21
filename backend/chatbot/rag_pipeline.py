# backend/chatbot/rag_pipeline.py
from typing import List, Dict
from embeddings.embedding_generator import EmbeddingGenerator
from embeddings.vector_store import VectorStore
from .llm_handler import LLMHandler
from .query_processor import QueryProcessor
from data_fetcher.data_gov_client import DataGovClient
from data_fetcher.data_processor import DataProcessor
from data_fetcher.cache_manager import CacheManager

class RAGPipeline:
    """RAG (Retrieval Augmented Generation) pipeline for Samarth"""
    
    def __init__(self):
        """Initialize RAG pipeline components"""
        print("Initializing RAG Pipeline...")
        
        # Initialize components
        self.embedding_generator = EmbeddingGenerator()
        self.vector_store = VectorStore(
            embedding_dim=self.embedding_generator.get_embedding_dim()
        )
        self.llm_handler = LLMHandler()
        self.query_processor = QueryProcessor()
        self.data_client = DataGovClient()
        self.data_processor = DataProcessor()
        self.cache_manager = CacheManager()
        
        # Try to load existing vector store
        if not self.vector_store.load():
            print("No existing vector store found. Will need to index data.")
            self.is_indexed = False
        else:
            self.is_indexed = True
        
        print("RAG Pipeline initialized successfully!")
    
    def index_data(self):
        """Index data from data.gov.in into vector store"""
        print("Starting data indexing...")
        
        # Fetch crop production data
        print("Fetching crop production data...")
        crop_data = self.data_client.fetch_crop_production()
        
        if crop_data:
            df_crop = self.data_processor.clean_crop_data(crop_data)
            crop_docs = self.data_processor.format_for_embedding(df_crop, 'crop')
            
            # Generate embeddings
            print(f"Generating embeddings for {len(crop_docs)} crop documents...")
            crop_texts = [doc['text'] for doc in crop_docs]
            crop_embeddings = self.embedding_generator.generate_embeddings(crop_texts)
            crop_metadata = [doc['metadata'] for doc in crop_docs]
            
            # Add to vector store
            self.vector_store.add_documents(crop_embeddings, crop_texts, crop_metadata)
        
        # Fetch rainfall data
        print("Fetching rainfall data...")
        rainfall_data = self.data_client.fetch_rainfall_data()
        
        if rainfall_data:
            df_rainfall = self.data_processor.clean_rainfall_data(rainfall_data)
            rainfall_docs = self.data_processor.format_for_embedding(df_rainfall, 'rainfall')
            
            # Generate embeddings
            print(f"Generating embeddings for {len(rainfall_docs)} rainfall documents...")
            rainfall_texts = [doc['text'] for doc in rainfall_docs]
            rainfall_embeddings = self.embedding_generator.generate_embeddings(rainfall_texts)
            rainfall_metadata = [doc['metadata'] for doc in rainfall_docs]
            
            # Add to vector store
            self.vector_store.add_documents(rainfall_embeddings, rainfall_texts, rainfall_metadata)
        
        # Save vector store
        self.vector_store.save()
        self.is_indexed = True
        
        print("Data indexing completed!")
        print(f"Total documents indexed: {self.vector_store.get_stats()['total_documents']}")
    
    def retrieve_context(self, query: str, k: int = 5) -> List[Dict]:
        """
        Retrieve relevant context for query
        
        Args:
            query: User query
            k: Number of documents to retrieve
            
        Returns:
            List of relevant documents with metadata
        """
        # Generate query embedding
        query_embedding = self.embedding_generator.generate_embedding(query)
        
        # Search vector store
        results = self.vector_store.search(query_embedding, k=k)
        
        return results
    
    def format_context(self, retrieved_docs: List[Dict]) -> str:
        """
        Format retrieved documents into context string
        
        Args:
            retrieved_docs: List of retrieved documents
            
        Returns:
            Formatted context string
        """
        context_parts = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            source = doc['metadata'].get('source', 'Unknown')
            doc_type = doc['metadata'].get('type', 'Unknown')
            
            context_parts.append(
                f"[Source {i}: {source}]\n"
                f"Type: {doc_type}\n"
                f"Content: {doc['document']}\n"
                f"Relevance Score: {doc['similarity']:.3f}\n"
            )
        
        return "\n\n".join(context_parts)
    
    def answer_query(self, query: str) -> Dict:
        """
        Answer user query using RAG pipeline
        
        Args:
            query: User query
            
        Returns:
            Dictionary with answer and sources
        """
        if not self.is_indexed:
            return {
                'answer': "The system is not yet indexed. Please run the indexing process first.",
                'sources': [],
                'query_info': {}
            }
        
        # Check cache
        cached_result = self.cache_manager.get('query', query=query)
        if cached_result:
            print("Returning cached result")
            return cached_result
        
        # Parse query
        query_info = self.query_processor.parse_query(query)
        
        # Retrieve relevant context
        retrieved_docs = self.retrieve_context(query, k=5)
        
        if not retrieved_docs:
            return {
                'answer': "I couldn't find relevant information in the database. Please try rephrasing your question.",
                'sources': [],
                'query_info': query_info
            }
        
        # Format context
        context = self.format_context(retrieved_docs)
        
        # Generate answer using LLM
        answer = self.llm_handler.generate_response(query, context)
        
        # Prepare sources
        sources = [
            {
                'text': doc['document'][:200] + '...',  # Truncate for display
                'source': doc['metadata'].get('source', 'Unknown'),
                'type': doc['metadata'].get('type', 'Unknown'),
                'metadata': doc['metadata'],
                'relevance': doc['similarity']
            }
            for doc in retrieved_docs
        ]
        
        result = {
            'answer': answer,
            'sources': sources,
            'query_info': query_info
        }
        
        # Cache result
        self.cache_manager.set('query', result, query=query)
        
        return result