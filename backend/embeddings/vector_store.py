# backend/embeddings/vector_store.py
import faiss
import numpy as np
import pickle
from typing import List, Dict, Tuple
import os

class VectorStore:
    """Vector store using FAISS for similarity search"""
    
    def __init__(self, embedding_dim: int, index_path: str = "vector_store"):
        """
        Initialize vector store
        
        Args:
            embedding_dim: Dimension of embeddings
            index_path: Path to save/load index
        """
        self.embedding_dim = embedding_dim
        self.index_path = index_path
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents = []
        self.metadata = []
        
    def add_documents(self, embeddings: np.ndarray, documents: List[str], 
                     metadata: List[Dict]):
        """
        Add documents to vector store
        
        Args:
            embeddings: Document embeddings
            documents: Document texts
            metadata: Document metadata
        """
        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')
        
        # Add to FAISS index
        self.index.add(embeddings)
        
        # Store documents and metadata
        self.documents.extend(documents)
        self.metadata.extend(metadata)
        
        print(f"Added {len(documents)} documents. Total: {self.index.ntotal}")
    
    def search(self, query_embedding: np.ndarray, k: int = 5) -> List[Dict]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding
            k: Number of results to return
            
        Returns:
            List of dictionaries containing documents and metadata
        """
        # Ensure query is float32 and 2D
        query_embedding = query_embedding.astype('float32').reshape(1, -1)
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, k)
        
        # Prepare results
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.documents):
                results.append({
                    'document': self.documents[idx],
                    'metadata': self.metadata[idx],
                    'distance': float(distances[0][i]),
                    'similarity': 1 / (1 + float(distances[0][i]))
                })
        
        return results
    
    def save(self):
        """Save vector store to disk"""
        os.makedirs(self.index_path, exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, os.path.join(self.index_path, "index.faiss"))
        
        # Save documents and metadata
        with open(os.path.join(self.index_path, "documents.pkl"), 'wb') as f:
            pickle.dump(self.documents, f)
        
        with open(os.path.join(self.index_path, "metadata.pkl"), 'wb') as f:
            pickle.dump(self.metadata, f)
        
        print(f"Vector store saved to {self.index_path}")
    
    def load(self):
        """Load vector store from disk"""
        if not os.path.exists(self.index_path):
            print(f"No saved index found at {self.index_path}")
            return False
        
        # Load FAISS index
        self.index = faiss.read_index(os.path.join(self.index_path, "index.faiss"))
        
        # Load documents and metadata
        with open(os.path.join(self.index_path, "documents.pkl"), 'rb') as f:
            self.documents = pickle.load(f)
        
        with open(os.path.join(self.index_path, "metadata.pkl"), 'rb') as f:
            self.metadata = pickle.load(f)
        
        print(f"Vector store loaded from {self.index_path}. Total documents: {len(self.documents)}")
        return True
    
    def get_stats(self) -> Dict:
        """Get vector store statistics"""
        return {
            'total_documents': len(self.documents),
            'embedding_dimension': self.embedding_dim,
            'index_size': self.index.ntotal
        }