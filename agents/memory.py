import chromadb
from chromadb.utils import embedding_functions
import json
import os
from datetime import datetime

# Initialize ChromaDB
# Persistent storage in 'memory_db' folder
chroma_client = chromadb.PersistentClient(path="./memory_db")

# Use a standard embedding model
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Get or create collection
collection = chroma_client.get_or_create_collection(
    name="llm_memory",
    embedding_function=sentence_transformer_ef
)

def add_to_memory(query: str, answer: str, source: str):
    """
    Save a Q&A pair to the vector database.
    """
    timestamp = datetime.now().isoformat()
    
    # Create a unique ID
    doc_id = f"{source}_{timestamp}"
    
    # We store the Q&A pair as the document text for retrieval
    document_text = f"Question: {query}\nAnswer: {answer}"
    
    collection.add(
        documents=[document_text],
        metadatas=[{"query": query, "answer": answer, "source": source, "timestamp": timestamp}],
        ids=[doc_id]
    )
    return True

def retrieve_context(query: str, n_results: int = 2):
    """
    Retrieve relevant past Q&A pairs for a given query.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    context = ""
    if results["documents"]:
        for i, doc in enumerate(results["documents"][0]):
            context += f"\n[Memory {i+1}]: {doc}\n"
            
    return context

def export_dataset(output_file: str = "training_data.jsonl"):
    """
    Export all memory items to a JSONL file for fine-tuning.
    Format: {"instruction": query, "input": "", "output": answer}
    """
    # Get all data
    all_data = collection.get()
    
    if not all_data["metadatas"]:
        return "No data to export."
        
    count = 0
    with open(output_file, "w", encoding="utf-8") as f:
        for metadata in all_data["metadatas"]:
            entry = {
                "instruction": metadata["query"],
                "input": "",
                "output": metadata["answer"],
                "source": metadata["source"]
            }
            f.write(json.dumps(entry) + "\n")
            count += 1
            
    return f"Exported {count} items to {output_file}"
