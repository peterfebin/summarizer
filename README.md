# summarize.py

A containerized CLI tool that summarizes any text file into 5–6 bullet points using a local LLM. No API keys. No internet required after setup. Works on any machine with Docker.

---

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Mac / Windows / Linux)

That's it.

---

## Setup

Clone or download this project, then navigate to the project folder:

```bash
cd summarizer
```

---

## Usage

Place the file you want to summarize in the project folder, then run:

```bash
docker-compose run --rm app -f /data/yourfile.txt
```

### Example

```bash
docker-compose run --rm app -f /data/report.txt
```

**Output:**

```
Summary of: report.txt
────────────────────────────────────────
• The report outlines Q3 revenue growth of 18% driven by enterprise sales.
• Customer churn decreased by 4% following the new onboarding initiative.
• Engineering headcount grew by 12 engineers across three teams.
• Two major product features shipped: AI search and bulk export.
• Infrastructure costs increased 22% due to GPU provisioning for ML workloads.
• Next quarter targets include entering the APAC market and closing Series B.
```

---

## First Run vs Subsequent Runs

### First run
The first run downloads the `llama3.2` model (~2GB). This happens once automatically and is cached in a Docker volume.

```
Pulling llama3.2 (first run only — this may take a few minutes)...
{"status":"pulling manifest"}
{"status":"pulling 8eeb52dfb3bb...","total":2019377152,"completed":...}
...
Model ready.
```

### Subsequent runs
The model is loaded from the local volume — no download, starts in seconds.

---

## Supported File Types

Any plain text file works:

| Type | Example |
|---|---|
| Plain text | `.txt` |
| Markdown | `.md` |
| Code | `.py`, `.js`, `.ts`, `.go` |
| Config / data | `.json`, `.yaml`, `.csv` |
| Logs | `.log` |

> Files larger than 100,000 characters are automatically truncated with a warning.

---

## How It Works

```
docker-compose run --rm app -f /data/file.txt
        ↓
  Ollama starts (local LLM server)
        ↓
  llama3.2 model loaded (downloaded on first run, cached after)
        ↓
  File is read from /data (your project folder, mounted into the container)
        ↓
  Content sent to llama3.2 with a summarization prompt
        ↓
  5–6 bullet points printed to your terminal
```

For a deeper look at the internals, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Stopping / Cleanup

Stop running containers:
```bash
docker-compose down
```

Remove everything including the downloaded model (frees ~2GB):
```bash
docker-compose down -v
```

---

## Troubleshooting

**"Cannot connect to Ollama"**
The Ollama service may not have started in time. Re-run the command — the health check usually resolves this.

**Summarization is slow**
The `llama3.2` (3B) model runs on CPU by default. On most laptops, expect 20–60 seconds for a medium-sized file.

**File not found**
Make sure your file is inside the project folder (the folder containing `docker-compose.yml`). That folder is mounted as `/data` inside the container.

```bash
# Wrong
docker-compose run --rm app -f /Users/febin/Downloads/myfile.txt

# Correct — copy file to project folder first, then:
docker-compose run --rm app -f /data/myfile.txt
```
