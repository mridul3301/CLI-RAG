from llama_index.llms import Ollama
import weaviate
import box
import yaml
from data_ingestion import load_documents, load_embedding_model, build_index

def build_pipeline(debug = False):
    # Import config vars
    with open('config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    # Connect to Weaviate
    print("Connecting to Weaviate.........")
    client = weaviate.Client(cfg.WEAVIATE_URL)
    
    # Load model from Ollama
    print("Loading Ollama.........")
    llm = Ollama(model=cfg.LLM, base_url=cfg.OLLAMA_BASE_URL, request_timeout=500.0)

    # Load the emnedding model of choice
    print("Loading embedding model.........")
    embeddings = load_embedding_model(model_name=cfg.EMBEDDINGS)
    
    # Load the documents
    print("Loading documents.........")
    documents = load_documents(cfg.DATA_PATH)

    # Build the index
    print("Building index.........")
    index = build_index(cfg.CHUNK_SIZE, llm, embeddings, client, documents, cfg.INDEX_NAME)
    print(f"Index created successfully! {index}")
    
    # Setup the query engine
    print("Setup Query Engine.........")
    query_engine = index.as_query_engine(streaming=True)
    print("Query Engine setup successful!")
    
    return query_engine