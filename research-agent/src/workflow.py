from typing import Any
from langgraph.graph import StateGraph, END, START
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from src.models import ResearchState, CompanyInfo, CompanyAnalysis
from src.firecrawl_service import FirecrawlService
from src.prompts import DeveloperToolsPrompts
from src.print_styles import print_error, print_info


class Workflow:
    def __init__(self, llm: BaseChatModel, firecrawl_service: FirecrawlService):
        self._firecrawl = firecrawl_service
        self._llm = llm
        self._developer_tools_prompt = DeveloperToolsPrompts()
        self._workflow = self._build_workflow()

    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)

        graph.add_edge(START, "extract_tools")
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)

        return graph.compile()

    def _extract_tools_step(self, state: ResearchState) -> dict[str, Any]:
        print_info(f"🔎 Finding articles about: {state.query}")

        article_query = f"{state.query} tools comparison best alternatives"
        search_result = self._firecrawl.search_companies(article_query, k_results=3)

        all_content = ""
        for result in search_result.data:
            url = result.get("url", "")

            if not url:
                continue

            scraped = self._firecrawl.scrape_company_pages(url=url)
            if scraped.success:
                all_content += scraped.markdown[:1500] + "\n\n"

        messages = [
            SystemMessage(content=self._developer_tools_prompt.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(
                content=self._developer_tools_prompt.tool_extraction_user(
                    state.query, all_content
                )
            ),
        ]

        try:
            response = self._llm.invoke(messages)
            tools_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            print_info(f"Extracted tools: {', '.join(tools_names[:5])}")
            return {"extracted_tools": tools_names}
        except Exception as e:
            print_error(str(e))
            return {"extracted_tools": []}

    def _analyze_company_content(
        self, company_name: str, content: str
    ) -> CompanyAnalysis:
        structured_llm = self._llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self._developer_tools_prompt.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(
                content=self._developer_tools_prompt.tool_analysis_user(
                    company_name=company_name, content=content
                )
            ),
        ]

        try:
            return structured_llm.invoke(messages)
        except Exception as e:
            print_error(e)
            return CompanyAnalysis(pricing_model="Unknown")

    def _research_step(self, state: ResearchState) -> dict[str, Any]:
        extracted_tools = getattr(state, "extracted_tools", [])
        if not extracted_tools:
            print_info("⚠️ No extracted tools found, falling back to direct search.")
            search_results = self._firecrawl.search_companies(state.query, k_results=4)
            tool_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            tool_names = extracted_tools[:4]

        print_info(f"🔬 researching specific tools: {', '.join(tool_names)}")
        companies = []
        for tool_name in tool_names:
            tool_search_result = self._firecrawl.search_companies(
                tool_name + " official site", k_results=1
            )
            if tool_search_result.success:
                result = tool_search_result.data[0]
                url = result.get("url", "")

                company = CompanyInfo(
                    name=tool_name,
                    description=result.get("markdown", ""),
                    website=url,
                    tech_stack=[],
                    competitors=[],
                )

                scraped = self._firecrawl.scrape_company_pages(url)
                if scraped:
                    content = scraped.markdown
                    analysis = self._analyze_company_content(company.name, content)

                    # Dynamically assigning all fields
                    company_fields = company.__class__.model_fields.keys()
                    for field, value in analysis.model_dump().items():
                        if field in company_fields:
                            setattr(company, field, value)

                companies.append(company)

        return {"companies": companies}

    def _analyze_step(self, state: ResearchState) -> dict[str, Any]:
        print_info("Generating recommendations")

        company_data = ", ".join(
            [company.model_dump_json() for company in state.companies]
        )

        messages = [
            SystemMessage(content=self._developer_tools_prompt.RECOMMENDATIONS_SYSTEM),
            HumanMessage(
                content=self._developer_tools_prompt.recommendations_user(state.query, company_data)
            ),
        ]

        response = self._llm.invoke(messages)
        return {"analysis": response.content}

    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self._workflow.invoke(initial_state)
        return ResearchState(**final_state)
