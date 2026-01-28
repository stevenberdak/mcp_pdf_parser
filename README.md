# mcp-pdf

Local-first MCP-style PDF ingestion + vector search + query, with both CLI and FastAPI.

## Author

Steven R Berdak
stevenberdak@gmail.com

## Read First

This repository was developed alongside an LLM in response to emerging requirements encountered while studying **RAG-based text generation**, **large language models**, and the **MCP design pattern**. It is intended to serve as a foundation for exploring and experimenting with LLM-related features and workflows.

While the repository does not include code for parsing vector store results directly through an LLM, it provides all the necessary components to enable such integration. For example, an LLM (such as one running via **Ollama**) can be layered on top to parse retrieved context from the **Chroma** vector store and generate coherent, context-aware text responses.

Query results are returned in **JSON format**, containing structured data that an LLM can consume to generate rich, contextual responses based on user-provided PDF documents.

## Example

**Query**
``` bash
mcp-pdf query "What are the ingredients to make Chulpe?"
```

**Response**
``` bash
{
  "action": "answer",
  "answer": "Top retrieved chunks:\n\n- (.\\mcp_pdf_parser\\pdf_files\\test_doc.pdf#p1#test_doc.pdf-47692-1769213449::p000001::c0000::f7b65ea709)\n  Peruvian Dried Corn (Chulpe)\n\n  Ingredients:\n  1. Bag of Peruvian dried corn\n  2. Pot with a cover\n  3. Cooking oil\n  4. Salt\n  5. (Optional) Additional spices\n\n  Instructions:\n  1. Add a generous amount of preferred oil to the bottom of the pot (olive oil recommended).\n  2. Heat oil on medium heat.\n\n- (.\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p1325#fas_crse_cat.pdf-4754896-1769117512::p001325::c0002::bee63f4a30)\n  MW 09:00 AM – 10:15 AM\n  Instructor: Ryan Nett\n\n  Life has evolved countless bioactive molecules, or \"natural products\", that act like pharmaceuticals to affect\n  cellular processes in other organisms. Many of these molecules serve as critical medicines and research tools.\n\n- (.\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p840#fas_crse_cat.pdf-4754896-1769117512::p000840::c0002::7874d1ed6d)\n  Culinary science-focused coursework exploring the chemistry and physics behind cooking techniques.\n  Students study the properties and behaviors of soft matter materials through food-based examples.\n\n- (.\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p257#fas_crse_cat.pdf-4754896-1769117512::p000257::c0002::460a29fc51)\n  Course content covering planning organic chemical syntheses with an introduction to organometallic chemistry.\n\n- (.\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p274#fas_crse_cat.pdf-4754896-1769117512::p000274::c0000::acb79503b8)\n  CHEM 398 — Organic and Organometallic Chemistry\n  Course ID: 122696\n  Credits: 4\n\n  2026 Spring: No meeting time listed (Instructor Permission Required)\n  2025 Fall: No meeting time listed (Instructor Permission Required)\n",
  "citations": [
    ".\\mcp_pdf_parser\\pdf_files\\test_doc.pdf#p1#test_doc.pdf-47692-1769213449::p000001::c0000::f7b65ea709",
    ".\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p1325#fas_crse_cat.pdf-4754896-1769117512::p001325::c0002::bee63f4a30",
    ".\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p840#fas_crse_cat.pdf-4754896-1769117512::p000840::c0002::7874d1ed6d",
    ".\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p257#fas_crse_cat.pdf-4754896-1769117512::p000257::c0002::460a29fc51",
    ".\\mcp_pdf_parser\\pdf_files\\fas_crse_cat.pdf#p274#fas_crse_cat.pdf-4754896-1769117512::p000274::c0000::acb79503b8"
  ]
}
```

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## Ingest PDFs (file or directory)
```bash
mcp-pdf ingest /path/to/file.pdf
mcp-pdf ingest /path/to/dir --force   # reindex even if unchanged
```

## Query from CLI
```bash
mcp-pdf query "What does it say about X?" --k 12
```

## Run API server
```bash
uvicorn mcp_pdf.api:app --reload
```

Then open:
- http://localhost:8000/docs