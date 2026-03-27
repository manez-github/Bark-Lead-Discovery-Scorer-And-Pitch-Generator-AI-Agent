import asyncio
import random 
import os

from dotenv import load_dotenv
load_dotenv()

import ctypes
import time
import threading

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

import ctypes
import time
import threading

def keep_awake():
    """
    Prevents Windows from sleeping while the script runs.
    This runs in a background thread.
    """
    # Windows API constant to prevent sleep
    ES_CONTINUOUS = 0x80000000
    ES_SYSTEM_REQUIRED = 0x00000001
    
    # Call the Windows API to tell the system "I am busy"
    ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
    print("☕ Windows Sleep Prevention: ENABLED")

