# 🔍 Developer Tools Research Workflow

This project provides a structured research workflow using a combination of LLMs (Large Language Models), web scraping, and structured analysis to **discover, research, and analyze software developer tools** based on a user-provided query.

## 🧠 What It Does

Given a query like "error monitoring tools", the system will:

1. **Search and extract tools** relevant to the query.
2. **Research individual tools**, scraping their websites for content.
3. **Analyze each tool** using an LLM to extract structured insights (e.g., pricing model, features).
4. **Generate a recommendation or summary** based on the analyzed tools.

---

## 🏗️ Components

### `Workflow` Class

Orchestrates the full research pipeline using a LangGraph state machine.

- **Dependencies**:
  - `langgraph` (for building the workflow)
  - `langchain` (for LLM interaction)
  - `src.models` (contains data models like `ResearchState`, `CompanyInfo`, `CompanyAnalysis`)
  - `src.firecrawl_service` (wraps search and scraping logic)
  - `src.prompts` (LLM prompt templates)
  - `src.print_styles` (console print helpers)

### Main Steps

- **`_extract_tools_step`**  
  Searches the web for articles and extracts tool names using LLMs.

- **`_research_step`**  
  For each tool:
  - Searches for the official site
  - Scrapes its content
  - Analyzes it via structured LLM output

- **`_analyze_step`**  
  Aggregates and summarizes tool data to generate user recommendations.

---

## 📝 Example Query

```bash
"frontend error tracking tools"
```

### Output

A list of tools like:
- Sentry
- Rollbar
- Bugsnag

With structured analysis on each and final recommendations.
