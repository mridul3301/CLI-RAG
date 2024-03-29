# CLI-RAG


## Usage :
Using the repo for RAG :

1. Clone the github repo: `https://github.com/mridul3301/CLI-RAG.git`

2. `cd` inside the repo

3. Run the following command `docker compose up -d` to set up vector database *weaviate*.

4. Install Ollama using command : `curl https://ollama.ai/install.sh | sh`

5. Run the following command : `ollama run <llm_name>`

3. Change the file inside the `data/` directory as necessary or leave as it is. All the documents inside `data/` should be in `.pdf` format.

4. Make personalized changes on stuff like “***LLM***” or “***EMBEDDINGS***” etc. by making changes on `congif.yml` file.

6. Run the file : `python rag.py`.

7. To exit qa terminal, type `exit` command.

## Information about code :
In this project, we are using `weaviate` as our vector database. The `docker-compose.yml` is actually used to set up weaviate client.

#### data_ingestion.py
In `data_ingestion.py`, we have methods to do following :
1. `load_documents` - Load the documents using `SimpleDirectoryReader`.
2. `load_embedding_model` - Load the embeddings model using `LangchainEmbedding`.
3. `build_index` - Builds the index for our documents using `ServiceContext`, `WeaviateVectorStore`, `StorageContext` & `VectorStoreIndex`.

#### pipeline.py
In `pipeline.py`, we build a pipeline that does following task :
1. Connects with weaviate client.
2. Load LLM model.
3. Load embeddings model.
4. Load the documents.
5. Build the index.
6. Setup the query engine.
 `pipeline.py` makes use of `data_ingestion.py`.

#### rag.py
`rag.py`is just used to infer the result.