from typing import Any
from firecrawl import FirecrawlApp, ScrapeOptions
from src.settings import Settings


class FirecrawlService:
    def __init__(self, settings: Settings):
        self._app = FirecrawlApp(api_key=settings.firecrawl_api_key)

    def search_companies(self, query: str, k_results: int = 5) -> dict[str, Any]:
        try:
            return self._app.search(
                query=f"{query} company pricing",
                limit=k_results,
                scrape_options=ScrapeOptions(formats=["markdown"]),
            )
        except Exception as e:
            return {"success": False, "data": [], "warning": None, "error": str(e)}

    def scrape_company_pages(self, url: str) -> dict[str, Any]:
        try:
            return self._app.scrape_url(url=url, formats=["markdown"])
        except Exception as e:
            return {"success": False, "data": [], "warning": None, "error": str(e)}
