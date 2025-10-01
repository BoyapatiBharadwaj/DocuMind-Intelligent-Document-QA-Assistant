# agents/llm_response_agent.py

from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOllama

class LLMResponseAgent:
    def __init__(self, model_name="llama3"):
        self.llm = ChatOllama(model=model_name)

    def generate_answer(self, query, retrieved_docs):
        print("🧠 LLM is generating response...")
        print("🔍 Query:", query)
        print("📄 Docs:", [doc.page_content[:100] for doc in retrieved_docs])

        chain = load_qa_chain(self.llm, chain_type="stuff")
        result = chain.run(input_documents=retrieved_docs, question=query)

        print("✅ Response:", result)
        return result
