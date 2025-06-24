from typing import Any, Literal, Optional
from pydantic import BaseModel, field_validator


class CompanyAnalysis(BaseModel):
    """Structured output for LLM company analysis focused on developer tools"""

    pricing_model: Literal["Free", "Freemium", "Paid", "Enterprise", "Unknown"]
    is_open_source: Optional[bool] = None
    tech_stack: list[str] = []
    description: str = ""
    api_available: Optional[bool] = None
    language_support: list[str] = []
    integration_capabilities: list[str] = []

    @field_validator("pricing_model", mode="before")
    @classmethod
    def normalize_pricing_model(cls, value: str) -> str:
        val = value.strip().lower()

        mapping = {
            "free": "Free",
            "freemium": "Freemium",
            "paid": "Paid",
            "enterprise": "Enterprise",
            "unknown": "Unknown",
        }

        return mapping.get(val, "Unknown")


class CompanyInfo(BaseModel):
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: list[str] = []
    competitors: list[str] = []
    # Developer-specific fields
    api_available: Optional[bool] = None
    language_support: list[str] = []
    integration_capabilities: list[str] = []
    developer_experience_rating: Optional[str] = None  # Poor, Good, Excellent


class ResearchState(BaseModel):
    query: str
    extracted_tools: list[str] = []  # Tools extracted from articles
    companies: list[CompanyInfo] = []
    search_results: list[dict[str, Any]] = []
    analysis: Optional[str] = None
