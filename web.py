import os
from groq import Groq
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
MODEL = "llama-3.1-8b-instant"
MAX_CHARS = 100_000


def call_groq(content):
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
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return response.choices[0].message.content


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    content = data.get("content", "").strip()

    if not content:
        return jsonify({"error": "No content provided"}), 400

    if len(content) > MAX_CHARS:
        content = content[:MAX_CHARS]

    try:
        summary = call_groq(content)
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
