from ..context.schema import ModelContext
from ..protocol.formats import Answer

def generate(ctx: ModelContext) -> Answer:
    # No LLM: return top retrieved snippets with citations.
    lines = []
    cites = []

    for r in ctx.retrieved[:5]:
        cite = f"{r.source}#p{r.page}#{r.chunk_id}"
        cites.append(cite)
        lines.append(f"- ({cite}) {r.text[:300]}")

    return Answer(
        answer="Top retrieved chunks:\n" + "\n".join(lines),
        citations=cites,
    )
