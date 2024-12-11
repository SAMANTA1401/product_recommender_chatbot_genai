from flask import Flask, render_template, request
from ecommercebot.data_ingestion import DataIngestion
from ecommercebot.retrieval_generation import RetrievalGeneration

embedding_model = "BAAI/bge-small-en-v1.5"
collection_name = "flipkart"
exists_collection = True
docs = None
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


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods = ["POST", "GET"])
def chat():
   
   if request.method == "POST":
      msg = request.form["msg"]
      input = msg

      result = conversational_rag_chain.invoke(
         {"input": input},
    config={
        "configurable": {"session_id": "abc123"}
    },
)["answer"]

      return str(result)







if __name__ == '__main__':
    
    app.run(port=5000, debug= True)  #host="0.0.0.0"