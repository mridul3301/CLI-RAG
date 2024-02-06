import weaviate
from llama_index import StorageContext, SimpleDirectoryReader, ServiceContext, VectorStoreIndex, SimpleNodeParser
from llama_index.vector_stores import WeaviateVectorStore
from llama_index.embeddings import LangchainEmbedding
from llama_index.llms import Ollama
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import box
import yaml
import warnings

# Hide the deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Read the documents from the data path using SimpleDirectoryReader
def load_documents(docs_path):
    # Load the PDF using the reader
    documents = SimpleDirectoryReader(docs_path, required_exts=[".pdf"]).load_data()
    print(f"Loaded {len(documents)} documents")
    print(f"First document: {documents[0]}")
    # chunk up the document into nodes
    parser = SimpleNodeParser.from_defaults(chunk_size=1024, chunk_overlap=20)
    nodes = parser.get_nodes_from_documents(documents)
    print("Successfully divided into chunks.")
    return nodes

# Load the embedding model from HuggingFace Embeddings & the name of embeddings is specified in config.yml
def load_embedding_model(model_name):
    embeddings = LangchainEmbedding(
        HuggingFaceEmbeddings(model_name=model_name)
    )
    return embeddings


# Index our documents 
def build_index(chunk_size, llm, weaviate_client, embed_model, nodes, index_name):
    # The service context container is a utility container for LlamaIndex index and query classes. 
    service_context = ServiceContext.from_defaults(chunk_size=chunk_size, embed_model=embed_model, llm=llm)
    # WeaviateVectorStore abstraction creates a central interface between our data abstractions and the Weaviate service. 
    vector_store = WeaviateVectorStore(weaviate_client=weaviate_client, index_name=index_name)
    # The storage context container is a utility container for storing nodes, indices, and vectors.
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Create the index
    index = VectorStoreIndex.from_documents(
        nodes,
        service_context=service_context,
        storage_context=storage_context,
    )

    print(f"Index created successfully!")
    return index


def build_rag_pipeline(debug = False):
    # Import config vars
    with open('config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    print("Connecting to Weaviate")
    client = weaviate.Client(cfg.WEAVIATE_URL)
    
    print("Loading Ollama...")
    llm = Ollama(model=cfg.LLM, base_url=cfg.OLLAMA_BASE_URL, temperature=0)

    print("Loading embedding model...")
    embeddings = load_embedding_model(model_name=cfg.EMBEDDINGS)
    
    print("Loading documents...")
    documents = load_documents(cfg.DATA_PATH)

    print("Building index...")
    index = build_index(cfg.CHUNK_SIZE, llm, client, embeddings, documents, cfg.INDEX_NAME)
    
    query_engine = index.as_query_engine(
        streaming=False,
        output_cls=InvoiceInfo,
        response_mode="compact"
    )

    