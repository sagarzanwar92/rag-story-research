**📖 AI Story Researcher: RAG with Hallucination Auditing**
A production-ready Retrieval-Augmented Generation (RAG) system designed to analyze complex narratives. This project features a unique dual-LLM architecture: one for story research and a second "Auditor" LLM to programmatically detect hallucinations and logical inconsistencies.
This is designed to be run on local systems with Ollama. The accuracy can hugely improve with better models, this one uses low size model to save space. 

**🌟 Key Features**
History-Aware Retrieval: Implements a standalone-query rewriter using langchain-classic to resolve pronouns and context across multi-turn conversations.
Temporal Logic Protection: Uses Chain-of-Thought (CoT) prompting to ensure the model respects chronological order (preventing common errors like setting a post-war story in the 1930s).
Automated Hallucination Audit: A dedicated hallucination_check.py script that uses LLM-as-a-Judge with a Chain-of-Verification (CoVe) rubric.
Structured Audit Logging: Every interaction logs the "RAG Triad" (User Query, Retrieved Context, and AI Answer) to a JSON file for offline performance analysis.
Stateless Backend: Powered by FastAPI, allowing for scalable deployment while maintaining conversation state in the Streamlit frontend.


**🛠️ Tech Stack**
LLM: Llama 3.2 (via Ollama)
Orchestration: LangChain (Classic)
Vector Database: ChromaDB
Embeddings: HuggingFace (all-MiniLM-L6-v2)
API: FastAPI & Uvicorn
UI: Streamlit

**🚀 Quick Start**
_1. Prerequisites_
Install Ollama and pull the model:
Bash: ollama pull llama3.2:1b

_2. Installation_
Bash: git clone https://github.com/sagarzanwar92/rag-story-researcher-public.git
cd rag-story-researcher-public
pip install -r requirements.txt

_3. Usage_
Place your PDF document in the root folder and rename it to short_story_pdf.pdf.
Ingest the data:
Bash: python ingest.py

Launch the System: Double-click run_all.bat or run the backend and frontend in separate terminals.

Audit for Hallucinations: After chatting, run the auditor to see if the AI lied:
Bash: python hallucination_check.py
----

📊 Evaluation & Safety
This project focuses on Faithfulness and Context Precision. By logging interactions, we can visualize where the model's reasoning breaks down. The audit_results.json provides a clear "Verdict" and "Reasoning" for every response generated.

🤝 Contributing
This is an open-source research project. Feel free to fork it, report hallucinations in the issues, or suggest better evaluation rubrics!
