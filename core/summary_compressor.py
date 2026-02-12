# core/summary_compressor.py

MAX_WORDS = 100

IMPORTANT_EXTENSIONS = (".py",)

def clean_text(text: str) -> str:
    text = text.replace("\n", " ").strip()
    while "  " in text:
        text = text.replace("  ", " ")
    return text

def compress_summary(text: str) -> str:
    words = clean_text(text).split()
    if len(words) <= MAX_WORDS:
        return " ".join(words)
    return " ".join(words[:MAX_WORDS]) + "..."

def compress_summaries(summaries, max_files=10):
    """
    Keep summaries short but meaningful.
    This feeds intent + planning agents safely.
    """

    compressed = []

    for s in summaries:
        file = s.get("file", "")
        summary = s.get("summary", "")

        if not file.endswith(IMPORTANT_EXTENSIONS):
            continue

        if not summary.strip():
            continue

        compressed.append({
            "file": file,
            "summary": compress_summary(summary),
        })

        if len(compressed) >= max_files:
            break

    return compressed
