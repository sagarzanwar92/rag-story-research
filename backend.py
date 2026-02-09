import json
import os
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

# LangChain Classic & Core
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI(title="RAG Master API with Auditing")

# 1. Setup Logging Directory
LOG_FILE = "interaction_logs.json"

def log_interaction(query, context, answer):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "retrieved_context": [doc.page_content for doc in context],
        "answer": answer
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    
    logs.append(log_entry)
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

# 2. Initialize RAG Components
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 3})
llm = ChatOllama(model="llama3.2:1b", temperature=0)

# 3. History-Aware Logic
context_prompt = ChatPromptTemplate.from_messages([
    ("system", "Formulate a standalone question based on history."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
history_aware_retriever = create_history_aware_retriever(llm, retriever, context_prompt)

# 4. QA Logic (Enhanced with Chain-of-Thought)
qa_system_prompt = (
    "You are a meticulous Story Research Assistant. Your goal is to provide logically "
    "consistent answers based ONLY on the provided context.\n\n"
    "Follow these steps to answer:\n"
    "1. ANALYZE: Identify all specific dates, historical events, and names in the context.\n"
    "2. TIMELINE: Determine the chronological order of these events.\n"
    "3. VERIFY: Ensure your conclusion (like the setting) does not contradict the latest date mentioned.\n"
    "4. ANSWER: Provide a concise conclusion based on the timeline.\n\n"
    "CONTEXT:\n{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])
# 4. QA Logic
# qa_prompt = ChatPromptTemplate.from_messages([
#     ("system", "Answer the question using the context: {context}"),
#     MessagesPlaceholder("chat_history"),
#     ("human", "{input}"),
# ])

doc_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, doc_chain)

class ChatMessage(BaseModel):
    role: str
    content: str

class QueryRequest(BaseModel):
    prompt: str
    history: List[ChatMessage] = []

@app.post("/ask")
async def ask_question(request: QueryRequest):
    try:
        chat_history = [
            HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
            for m in request.history
        ]
        
        # We invoke the chain to get the full result dictionary
        result = rag_chain.invoke({"input": request.prompt, "chat_history": chat_history})
        
        # LOGGING: Save the interaction for hallucination analysis
        log_interaction(request.prompt, result.get("context", []), result["answer"])
        
        return {"answer": result["answer"]}
        
    except Exception as e:
        print(f"Log Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)