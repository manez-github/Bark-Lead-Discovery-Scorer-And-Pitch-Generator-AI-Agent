import asyncio
import random 
from playwright.async_api import async_playwright
import os
from dotenv import load_dotenv
load_dotenv()

# Random human-like delay to avoid bot detection
async def human_delay(min_sec: float=0.3, max_sec: float=1.0):
    await asyncio.sleep(random.uniform(min_sec, max_sec))

# Move mouse like a human would   
async def human_mouse_move(page, target_x: float, target_y: float):
    steps = random.randint(10, 30)
    await page.mouse.move(target_x, target_y, steps=steps)

# Human like typing on a locator 
async def human_type(element, text: str):
    await element.click()
    await element.press_sequentially(text, delay=random.uniform(55, 170))
    await asyncio.sleep(random.uniform(0.15, 0.65))
    
GMAIL_ID = os.getenv("GMAIL_ID")
GMAIL_PASS = os.getenv("GMAIL_PASS")

async def login_to_bark_with_oauth():
    async with async_playwright() as p:          # Open browser using playwright
        context = await p.chromium.launch_persistent_context(
            user_data_dir="./browser_data",      # Saves session here
            headless=False,
            viewport={'width': 1280, 'height':720}, 
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            args=['--disable-blink-features=AutomationControlled']     # Hides automation
        )
        page = context.pages[0]
        
        # Navigate to login page. If already logged in, this usually redirects to dashboard
        print("Navigating to Bark.com login")
        await page.goto("https://www.bark.com/login/", wait_until="domcontentloaded")
        await human_delay(2, 4)
        
        # =============== CHECK IF ALREADY LOGGED IN ===================================
        dashboard_link = page.get_by_role("link", name="Dashboard")
        
        if await dashboard_link.is_visible(timeout=15000):
            print("✅ Already logged in. Skipping OAuth.")
        else:
            # ====== IF NOT LOGGED IN, PROCEED WITH GOOGLE LOGIN ======
            # Click on Login with Google
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
            
            await asyncio.sleep(60)
            await context.close()
        
if __name__ == "__main__":
    asyncio.run(login_to_bark_with_oauth())
        