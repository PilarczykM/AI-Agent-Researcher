## 🔍 Developer Tools Research Workflow

**Developer Tools Research Workflow** is an AI-powered research agent that automates the discovery, investigation, and analysis of software developer tools based on a user-provided query.

Built with LangGraph and LangChain, it combines LLMs, web scraping, and structured prompts to produce actionable insights on tools like *Sentry*, *Rollbar*, or *Bugsnag* — all from a single input like:

```bash
"frontend error tracking tools"
```

---

### 🔧 Key Features

- **Automated tool discovery** via web search + LLM parsing  
- **Website scraping & analysis** for each tool using custom logic  
- **Structured insights**: pricing, features, and positioning  
- **Final recommendations** summarized by an LLM  

---

### 🧠 How It Works

1. **Extract tool names** from web content using LLMs  
2. **Scrape and analyze** each tool’s website  
3. **Generate structured data & recommendations**

---

### 🔁 Powered By

- **LangGraph** – orchestrates the research flow  
- **LangChain** – for LLM interactions  
- **Custom modules** – search, scraping, data modeling, and prompts

---

Perfect for anyone building market maps, doing competitive research, or evaluating dev tooling options.
