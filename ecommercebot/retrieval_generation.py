from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains import create_history_aware_retriever
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory





from dotenv import load_dotenv
import os
load_dotenv()

os.environ["GROQ_API_KEY"]= os.getenv("groqe_api_key")

class RetrievalGeneration():
    def __init__(self, llm, temp,retriever_prompt,BOT_TEMPLATE,vstore,session_id:str):
        self.llm = llm
        self.temp = temp
        self.retriever_prompt = retriever_prompt
        self.BOT_TEMPLATE = BOT_TEMPLATE
        self.vstore = vstore
        self.store = {}
        self.chat_history= []
        self.session_id = session_id

    def llm_model(self):
        llm = ChatGroq(temperature=self.temp, model_name=self.llm)
        return llm
    
  

    def get_session_history(self)-> BaseChatMessageHistory:
        if self.session_id not in self.store:
            self.store[self.session_id]= ChatMessageHistory(messages=[])
        print(self.store)
        return self.store[self.session_id]
    
    def generation(self):
        retriever = self.vstore.as_retriever(search_kwargs={"k": 3})

        retriever_prompt = self.retriever_prompt

        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
            ("system", retriever_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            ]
        )
        
        # {context}
        history_aware_retriever = create_history_aware_retriever(self.llm_model(), retriever, contextualize_q_prompt)

        PRODUCT_BOT_TEMPLATE = self.BOT_TEMPLATE

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", PRODUCT_BOT_TEMPLATE),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}")
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm_model(), qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            self.get_session_history,  #pydantic_core._pydantic_core.ValidationError: 1 validation error for RunnableWithMessageHistory
                                        # get_session_history
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )

        return conversational_rag_chain
    

if __name__ == "__main__":
    pass
   

#    vstore = data_ingestion("done")
#    conversational_rag_chain = generation(vstore)
#    answer= conversational_rag_chain.invoke(
#     {"input": "can you tell me the best bluetooth buds?"},
#     config={
#         "configurable": {"session_id": "dhruv"}
#     },  # constructs a key "abc123" in `store`.
# )["answer"]
#    print(answer)
#    answer1= conversational_rag_chain.invoke(
#     {"input": "what is my previous question?"},
#     config={
#         "configurable": {"session_id": "dhruv"}
#     },  # constructs a key "abc123" in `store`.
# )["answer"]
#    print(answer1)

