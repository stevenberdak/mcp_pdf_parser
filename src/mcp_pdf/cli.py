import argparse
from pathlib import Path

from .core.ingest import ingest_directory, ingest_pdf
from .context.assembler import assemble_context
from .model.simple_answer import generate


def main():
    p = argparse.ArgumentParser(prog="mcp-pdf")
    sub = p.add_subparsers(dest="cmd", required=True)

    ing = sub.add_parser("ingest", help="Ingest a PDF file or a directory of PDFs recursively.")
    ing.add_argument("path", type=str, help="PDF file path or directory path")
    ing.add_argument("--force", action="store_true", help="Re-ingest even if fingerprint unchanged")

    q = sub.add_parser("query", help="Query the local vector store.")
    q.add_argument("text", type=str, help="Query text")
    q.add_argument("--k", type=int, default=10, help="Top-k results")

    args = p.parse_args()

    if args.cmd == "ingest":
        path = Path(args.path)
        if path.is_dir():
            print(ingest_directory(path, force=args.force))
        else:
            print(ingest_pdf(path, force=args.force))

    elif args.cmd == "query":
        ctx = assemble_context(args.text, top_k=args.k)
        print(generate(ctx).model_dump_json(indent=2))
