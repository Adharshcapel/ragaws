from fastapi import FastAPI
from backend import query_kb

app = FastAPI()

@app.get("/")
def home():
    return {"message": "RAG API Running"}

@app.post("/query")
def query(question: str):
    answer, sources = query_kb(question)
    return {"answer": answer, "sources": sources}

@app.get("/health")
def health():
    return {"status":"healthy"}
