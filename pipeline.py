from ecommercebot.data_converter import DataConverter
from ecommercebot.data_ingestion import DataIngestion
from ecommercebot.retrieval_generation import RetrievalGeneration




data_dir = 'artifacts/flipkart_product_review.csv'
columns = ['product_title', 'review']
meta_data = 'product_name'
page_content = 'review'
doc_converter = DataConverter(data_dir=data_dir, meta_data=meta_data, page_content=page_content, columns=columns)
documents = doc_converter.dataconverter()
print(documents[:1])


embedding_model = "BAAI/bge-small-en-v1.5"
collection_name = "flipkart"
exists_collection = False
docs = documents
data_ingest = DataIngestion(embedding_model=embedding_model, collection_name=collection_name, exists_collection=exists_collection, docs = docs)
vstore = data_ingest.data_ingestion()



llm = "llama-3.1-70b-versatile"
temp = 0.5
retriever_prompt= ( "Given a chat history and the latest user question which might reference context in the chat history,"
    "formulate a standalone question which can be understood without the chat history."
    "Do NOT answer the question, just reformulate it if needed and otherwise return it as is.")
BOT_TEMPLATE = """
    Your ecommercebot bot is an expert in product recommendations and customer queries.
    It analyzes product titles and reviews to provide accurate and helpful responses.
    Ensure your answers are relevant to the product context and refrain from straying off-topic.
    Your responses should be concise and informative.

    CONTEXT:
    {context}

    QUESTION: {input}

    YOUR ANSWER:

    """

# {context} history aware retriever contain input and chat history


session_id = "abc123"  # unique identifier for each user session.
ret_gen = RetrievalGeneration(llm=llm, temp=temp, retriever_prompt=retriever_prompt, BOT_TEMPLATE=BOT_TEMPLATE, vstore=vstore, session_id=session_id)


conversational_rag_chain = ret_gen.generation()



answer= conversational_rag_chain.invoke(
    {"input": "can you tell me the best bluetooth buds?"},
    config={
        "configurable": {"session_id": "abc123"}
    },  # constructs a key "abc123" in `store`.
)["answer"]
print(answer)
answer1= conversational_rag_chain.invoke(
{"input": "what is my previous question?"},
config={
    "configurable": {"session_id": "abc123"}
},  # constructs a key "abc123" in `store`.
)["answer"]
print(answer1)