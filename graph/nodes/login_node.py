import asyncio
from playwright.async_api import async_playwright

from utils.helpers import *
from graph.states import *

async def login_node(state: AgentState) -> dict:
    # ====== IF NOT LOGGED IN, PROCEED WITH GOOGLE LOGIN ======
    # Click on Login with Google
    page = state['page']
    print("Clicking Login with Google OAuth button...")
    google_button = page.get_by_role("button", name="Login with Google", exact=True)
    await google_button.scroll_into_view_if_needed()

    # Get the button's actual position. Button => Login with Google
    box = await google_button.bounding_box()
    """
    box looks something like this: 
    {
        'x': 150.5,      # Distance from the left edge of the page
        'y': 300.0,      # Distance from the top edge of the page
        'width': 200.0,  # Width of the button
        'height': 40.0   # Height of the button
    }
    """
    # Point the mouse directly towards the center of the box
    target_x = box['x'] + box['width'] / 2
    target_y = box['y'] + box['height'] / 2

    # Move smoothly to that exact position
    await human_mouse_move(page, target_x, target_y)


    await page.mouse.click(target_x, target_y)    
    await human_delay(3, 5)

    # ============== GOOGLE OAUTH FLOW ======================
    await page.wait_for_url("**accounts.google.com**", timeout=30000)
    print("Google popup opened successfully")

    # When accounts.google.com loads in the first page we type our gmail id
    print("Entering gmail id")
    email_input = page.get_by_role("textbox", name="Email or phone")
    await human_type(email_input, GMAIL_ID)
    await human_delay(1, 2)

    # Get the next button
    next_button = page.get_by_role("button", name="Next")

    # Get the button's actual position. Button => Next
    box = await next_button.bounding_box()

    # Point the mouse directly towards the center of the box
    target_x = box['x'] + box['width'] / 2
    target_y = box['y'] + box['height'] / 2

    # Move smoothly to that exact position
    await human_mouse_move(page, target_x, target_y)
    await page.mouse.click(target_x, target_y)

    await human_delay(3, 5)

    # Type the password on the next page
    print("Entering password")
    password_input = page.get_by_role("textbox", name="Enter your password")
    await human_type(password_input, GMAIL_PASS)
    await human_delay(1, 2)

    # Get the next button
    next_button = page.get_by_role("button", name="Next")

    # Get the button's actual position. Button => Next
    box = await next_button.bounding_box()

    # Point the mouse directly towards the center of the box
    target_x = box['x'] + box['width'] / 2
    target_y = box['y'] + box['height'] / 2

    # Move smoothly to that exact position
    await human_mouse_move(page, target_x, target_y)
    await page.mouse.click(target_x, target_y)

    await human_delay(3, 5)

    await page.wait_for_url("**bark.com**", timeout=30000)

    # Verify we logged in
    if await page.get_by_text("Dashboard").is_visible(timeout=15000):
        print("✅ Successfully Logged in")
    else:
        print("⚠️ Login may have succeded but dashboard not detected yet.")