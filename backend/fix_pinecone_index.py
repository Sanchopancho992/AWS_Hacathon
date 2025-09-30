import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def fix_pinecone_index():
    """Delete and recreate Pinecone index with correct dimensions for Gemini embeddings"""
    
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    if not pinecone_api_key:
        print("ERROR: PINECONE_API_KEY not found in environment variables")
        return False
    
    # Initialize Pinecone
    pc = Pinecone(api_key=pinecone_api_key)
    
    index_name = "awshacathon"
    
    try:
        # Check if index exists
        existing_indexes = pc.list_indexes()
        index_exists = any(idx.name == index_name for idx in existing_indexes)
        
        if index_exists:
            print(f"Deleting existing index '{index_name}' with wrong dimensions...")
            pc.delete_index(index_name)
            print("Index deleted successfully")
            
            # Wait for deletion to complete
            print("Waiting for deletion to complete...")
            time.sleep(10)
        
        # Create new index with correct dimensions for Gemini embeddings (768)
        print(f"Creating new index '{index_name}' with 768 dimensions for Gemini embeddings...")
        
        pc.create_index(
            name=index_name,
            dimension=768,  # Google Gemini embedding dimension
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
        
        print("Index created successfully!")
        
        # Wait for index to be ready
        print("Waiting for index to be ready...")
        time.sleep(30)
        
        # Verify the index
        index = pc.Index(index_name)
        stats = index.describe_index_stats()
        print(f"Index stats: {stats}")
        print(f"✅ SUCCESS: Index '{index_name}' is ready with 768 dimensions!")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Failed to fix Pinecone index: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Fixing Pinecone index dimensions for Google Gemini embeddings...")
    success = fix_pinecone_index()
    if success:
        print("🎉 Pinecone index fixed! Your RAG service should work now.")
    else:
        print("💥 Failed to fix Pinecone index. Check your API key and try again.")
