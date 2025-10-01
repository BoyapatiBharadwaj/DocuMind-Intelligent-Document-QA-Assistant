# ui/streamlit_app.py

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import tempfile
import os
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
from mcp.context_protocol import MCPMessage

st.title("📚 Agentic RAG Chatbot with MCP")

uploaded_files = st.file_uploader("Upload Documents", accept_multiple_files=True)
query = st.text_input("Ask a question:")

if "vector_ready" not in st.session_state:
    st.session_state.vector_ready = False

# Init agents
ingestion_agent = IngestionAgent()
retrieval_agent = RetrievalAgent()
llm_agent = LLMResponseAgent()

if uploaded_files:
    file_paths = []
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in uploaded_files:
            file_path = os.path.join(temp_dir, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())
            file_paths.append(file_path)

        docs = ingestion_agent.load_documents(file_paths)
        retrieval_agent.build_vectorstore(docs)
        st.session_state.vector_ready = True
        st.success("Documents ingested and indexed!")

if query and st.session_state.vector_ready:
    top_docs = retrieval_agent.retrieve_context(query)
    
    # MCP Message creation
    mcp = MCPMessage(
        sender="RetrievalAgent",
        receiver="LLMResponseAgent",
        msg_type="RETRIEVAL_RESULT",
        payload={"retrieved_context": [doc.page_content for doc in top_docs], "query": query}
    )

    st.json(mcp.get_message())  # Optional debug output

    response = llm_agent.generate_answer(query, top_docs)
    st.markdown("### 🤖 Answer")
    st.write(response)
