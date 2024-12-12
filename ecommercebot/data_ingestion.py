from langchain_astradb import AstraDBVectorStore
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()


os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.environ["LANGCHAIN_API_KEY"]
ASTRA_DB_API_ENDPOINT = os.environ["ASTRA_DB_API_ENDPOINT"]
ASTRA_DB_APPLICATION_TOKEN = os.environ.get("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.environ.get("ASTRA_DB_KEYSPACE")
GROQ_API_KEY = os.environ['GROQE_API_KEY']
HF_TOKEN = os.environ["HF_ACCESS_TOKEN"]


class DataIngestion():
    def __init__(self,embedding_model,collection_name,exists_collection,docs):
        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.docs = docs
        self.exists_collection = exists_collection


    def embedding(self):
        embedding_model = HuggingFaceInferenceAPIEmbeddings(
            api_key=HF_TOKEN,
            model_name=self.embedding_model
        )
        return embedding_model
    
    def data_ingestion(self):
        vstore = AstraDBVectorStore(
               embedding=self.embedding(),
               collection_name=self.collection_name,
               api_endpoint=ASTRA_DB_API_ENDPOINT,
               token=ASTRA_DB_APPLICATION_TOKEN,
               namespace=ASTRA_DB_KEYSPACE,
               )
        
        if self.exists_collection:
            if self.docs == None:
                print("No documents to ingest")
                return vstore
            else:
                print("Ingesting documents")
                vstore.add_documents(self.docs)
                return vstore
            
        vstore.add_documents(self.docs)

        return vstore

       
        
    

if __name__ == "__main__":
    # embedding_model = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_model = "BAAI/bge-small-en-v1.5"
    # storage_status = None
    collection_name = "flipkart"

    docs = None

    data_ingest = DataIngestion(embedding_model=embedding_model, collection_name=collection_name, exists_collection=True, docs = docs)
    vstore = data_ingest.data_ingestion()
    results = vstore.similarity_search("Can you tell me the low budget sound basshead?")
    for res in results:
        print(f"\n {res.page_content} [{res.metadata}]")
