# 🔥 LangChain Firecrawl Agent (MVP)

A minimal command-line assistant that uses [LangChain](https://www.langchain.com/), [OpenAI GPT-4o](https://openai.com/), and [Firecrawl](https://firecrawl.dev) to crawl and scrape websites using MCP (Modular Command Platform) tools.

This is a **simpler MVP version**, focused on getting core functionality working with clean CLI interaction and minimal setup. Dependency management is handled with [`uv`](https://github.com/astral-sh/uv).

---

## ✨ Features

- GPT-4o-mini-powered assistant
- Crawl and scrape websites using Firecrawl MCP tools
- Dynamic tool loading and execution via MCP
- Async event loop for non-blocking behavior
- Clean terminal interface with styled input/output
- Simple architecture for rapid prototyping

---

## 🧠 Tech Stack

- **LangChain + LangGraph** for agent orchestration
- **OpenAI GPT-4o-mini** as the LLM
- **Firecrawl MCP** for data extraction and crawling
- **uv** for fast Python dependency and script management
- **asyncio** for concurrent CLI interaction

---

## ⚙️ Setup

### 1. Install `uv`

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

### 2. Install project dependencies

```bash
uv pip install -r pyproject.toml
```

or

```bash
uv sync
```

### 3. Set up environment variables

Create a `.env` file or ensure `settings.py` provides the following:

```env
OPENAI_API_KEY=your_openai_key
FIRECRAWL_API_KEY=your_firecrawl_key
```

---

## ▶️ Run the Assistant

```bash
uv run main.py
```

---

## 💬 Example Prompts

```
Scrape the main headlines from https://example.com
Crawl https://openai.com and list all internal links
```

Type `quit` or press `Ctrl+C` to exit.

---

## 📁 Project Structure

```
.
├── main.py              # Main agent loop
├── settings.py          # Loads API keys
├── print_styles.py      # CLI I/O helpers
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # You're here!
```

---

## 🧪 Notes

- This is a **minimal MVP**—great for testing, prototyping, and exploring Firecrawl + LangChain integrations.
- Not intended for production use (yet)—no persistent storage, caching, or advanced tool chaining.
- Easily extendable with memory, context management, or richer toolsets.
