import asyncio
from graph.states import *

async def close_node(state: AgentState):
    """
    Closes the browser context and stops the Playwright instance.
    """
    print("--- NODE: CLOSE---")
    
    context = state.get('browser_context')
    p = state.get('playwright_instance')
    
    # Close the browser context
    await context.close()
    
    # Stop playwright instance
    await p.stop()
    
    return {'next_action': 'exit'}