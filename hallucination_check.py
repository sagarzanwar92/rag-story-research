import json
import os
from datetime import datetime
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

# 1. Initialize the "Judge" LLM
llm = ChatOllama(model="llama3.2:1b", temperature=0)

def save_audit_results(results):
    AUDIT_FILE = "audit_results.json"
    with open(AUDIT_FILE, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\n✅ Audit complete. Verdicts saved to {AUDIT_FILE}")

def verify_hallucinations():
    LOG_FILE = "interaction_logs.json"
    
    if not os.path.exists(LOG_FILE):
        print("No logs found. Chat with the AI first to generate interaction_logs.json!")
        return

    with open(LOG_FILE, "r") as f:
        logs = json.load(f)

    audit_records = []
    print(f"--- Auditing {len(logs)} Interactions ---\n")

    judge_prompt = ChatPromptTemplate.from_template("""
    ### STEP 1: EXTRACT DATES
    List every date or year mentioned in the CONTEXT.
    List every date or year mentioned in the ANSWER.

    ### STEP 2: LOGICAL CHECK
    Does any date in the ANSWER happen BEFORE the dates in the CONTEXT?
    Is the setting mentioned in the ANSWER consistent with the dates in the CONTEXT?

    ### STEP 3: VERDICT
    If any date or historical setting is wrong, label as 'HALLUCINATION'. 
    Otherwise, if it matches exactly, label as 'FAITHFUL'.

    CONTEXT: {context}
    ANSWER: {answer}

    VERDICT:
    REASONING:
    """)


    for entry in logs:
        context_text = " ".join(entry["retrieved_context"])
        
        chain = judge_prompt | llm
        response = chain.invoke({"context": context_text, "answer": entry["answer"]})
        
        # Create the record
        audit_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": entry["query"],
            "original_answer": entry["answer"],
            "verdict": response.content.strip()
        }
        audit_records.append(audit_entry)
        
        print(f"Query: {entry['query']}")
        print(f"Result: {response.content.strip()} \n" + "-"*30)

    save_audit_results(audit_records)
    

if __name__ == "__main__":
    verify_hallucinations()
    