from graph.states import *
from utils.helpers import *

async def auth_check_node(state: AgentState) -> dict:
    
    page = state['page']
    
    # Navigate to login page. If already logged in, this usually redirects to dashboard
    await page.goto("https://www.bark.com/login/", wait_until="domcontentloaded")
    await human_delay(4, 5)
    
    dashboard_link = page.get_by_role("link", name="Dashboard")
    
    is_logged_in = await dashboard_link.is_visible(timeout=30000)
    
    if is_logged_in:
        print("User is logged in.")
        return {"next_action": "scrape"}
    else: 
        print("User is NOT logged in.")
        return {"next_action": "login"}
    
    
    