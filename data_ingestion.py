from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import warnings

# Hide the deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Read the documents from the data path using SimpleDirectoryReader
def load_documents(docs_path):
    # Load the PDF using the reader
    documents = SimpleDirectoryReader(docs_path).load_data()
    print(f"Loaded {len(documents)} documents")
    return documents


# Load the embedding model from HuggingFace Embeddings & the name of embeddings is specified in config.yml
def load_embedding_model(model_name):
    embeddings = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name=model_name)
    )
    return embeddings


# Index our documents 
def build_index(chunk_size, llm, embed_model, weaviate_client, documents, index_name):
    
    service_context = ServiceContext.from_defaults(
        chunk_size=chunk_size,
        llm=llm,
        embed_model=embed_model
    )
    
    # WeaviateVectorStore abstraction creates a central interface between our data abstractions and the Weaviate service. 
    vector_store = WeaviateVectorStore(weaviate_client=weaviate_client, index_name=index_name)
    
    # The storage context container is a utility container for storing documents, indices, and vectors.
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Create the index
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)
    
    print(f"Index created successfully!")
    
    return index