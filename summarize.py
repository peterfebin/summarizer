import argparse
import os
import sys
from groq import Groq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"
MAX_CHARS = 100_000


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize a file into bullet points")
    parser.add_argument("--file", "-f", required=True, help="Path to the file to summarize")
    return parser.parse_args()


def read_file(path):
    if not os.path.exists(path):
        print(f"Error: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    if len(content) > MAX_CHARS:
        print(f"Warning: File is large, truncating to {MAX_CHARS} characters.", file=sys.stderr)
        content = content[:MAX_CHARS]

    return content


def summarize(content):
    prompt = (
        "You are a summarization assistant. Summarize the content below into exactly 6 points.\n"
        "Rules:\n"
        "- Write exactly 6 points. Not 2. Not 4. Exactly 6.\n"
        "- Each point must begin with EXACTLY ONE '•' character followed by a single space, then the text.\n"
        "- Do not add any other prefix, dash, marker, or symbol before or after the '•'.\n"
        "- Each point is one concise sentence covering a key idea or theme.\n"
        "- Output only the 6 points. No introduction, no conclusion, no extra text.\n\n"
        f"Content:\n{content}"
    )
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq: {e}", file=sys.stderr)
        sys.exit(1)


def print_summary(filename, summary):
    print(f"\nSummary of: {os.path.basename(filename)}")
    print("─" * 40)
    print(summary)
    print()


def main():
    args = parse_args()
    content = read_file(args.file)
    summary = summarize(content)
    print_summary(args.file, summary)


if __name__ == "__main__":
    main()
