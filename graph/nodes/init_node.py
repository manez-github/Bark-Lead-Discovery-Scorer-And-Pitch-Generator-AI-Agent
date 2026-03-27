from graph.states import *
from playwright.async_api import async_playwright

async def init_node(state: AgentState) -> dict:
    """ 
    Launches persistent_browser_context.
    Gives plarywright_instance, BrowserContext and Page to AgentState
    """
    print("--- NODE: INIT ---")
    print("launch_persistent_context")
    
    p = await async_playwright().start()
    
    # Launch Persistent Context (This replaces browser.launch + context.new_context)
    context = await p.chromium.launch_persistent_context(
        user_data_dir="./browser_data",
        headless=False,
        viewport={'width': 1280, 'height': 720},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        args=['--disable-blink-features=AutomationControllined'] 
    )
    
    # Get the first page (tab)
    if len(context.pages) > 0:
        page = context.pages[0]
    else:
        page = await context.new_page()
        
    return {
        "playwright_instance": p,
        "browser_context": context,
        "page": page
    }