from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

from .core.ingest import ingest_directory, ingest_pdf
from .context.assembler import assemble_context
from .model.simple_answer import generate

app = FastAPI(title="mcp_pdf")

class IngestRequest(BaseModel):
    path: str
    force: bool = False

class QueryRequest(BaseModel):
    query: str
    k: int = 10

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
def ingest(req: IngestRequest):
    p = Path(req.path)
    if p.is_dir():
        return ingest_directory(p, force=req.force)
    return ingest_pdf(p, force=req.force)

@app.post("/query")
def query(req: QueryRequest):
    ctx = assemble_context(req.query, top_k=req.k)
    return generate(ctx).model_dump()
