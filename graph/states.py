from typing import TypedDict, Optional, Any
from playwright.async_api import Playwright, BrowserContext, Page
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    """
    Shared memory of the agent. 
    Holds references to the browser and data collected.
    """
    playwright_instance: Optional[Playwright] 
    browser_context: Optional[BrowserContext] 
    page: Optional[Page]
    next_action: str

    
class LeadScore(BaseModel):
    score: float = Field(description="Score from 0.0 to 1.0 indicating fit.")
    reasoning: str = Field(description="Brief explanation of why this score was given")
    is_qualified: bool = Field(description="Ture if score>=0.8")