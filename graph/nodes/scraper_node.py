import os
import json
from typing import Dict

from graph.states import *
from utils.helpers import *
from utils.database import *

async def scraper_node(state: AgentState) -> Dict:
    print("--- NODE: SCRAPER ---")
    
    # Existing ids
    existing_leads = load_existing_leads()
    existing_ids = {lead['id'] for lead in existing_leads}
    print(f"Loaded {len(existing_ids)} from JSON")
    
    # New leads count 
    new_leads_count = 0
    
    page = state['page']

    print("Navigating to Leads")
    await page.goto("https://www.bark.com/sellers/dashboard/", wait_until="domcontentloaded") 
    await human_delay(15, 20)       
    
    # list_container => Scroll bar of the container/ panel to the left.
    # This also has other buttons like filter, edit, etc apart from the leads buttons
    scroll_container = page.locator("#dashboard-projects")
    
    print("Scrolling to load all leads...")
    last_height = 0
    while True:
        # Scroll the html element to the left which contains all the leads down
        await scroll_container.evaluate("el => el.scrollTop = el.scrollHeight")
        await human_delay(12, 15)
        
        new_height = await scroll_container.evaluate("el => el.scrollHeight")
        if new_height == last_height:
            print("Reached the bottom.")
            break
        last_height = new_height
        
    # Again scroll to the top because we cannot be at the bottom and click on button 1
    # We scrolled down to load all the buttons so that we can get the all the number of leads that we have
    
    await scroll_container.evaluate("el => el.scrollTop = 0")
    await human_delay(12, 15)
    
    # The INNER container (Holds only the lead buttons)
    # Used for: Selecting buttons to click
    leads_list_container = scroll_container.locator("div[data-cy='leads-list']")
    
    # lead_buttons is a list where each element is a locator object related to a specific button
    lead_buttons = await leads_list_container.locator("button").all()
    print(f"Found {len(lead_buttons)} leads. Starting processing...")

    for i, button in enumerate(lead_buttons):
        box = await button.bounding_box()
        
        viewport_height = page.viewport_size['height']
        if box['y'] > viewport_height:
            print("This lead is not visible. Scrolling to its locatiion...")
            # Code to smoothly 
            await scroll_container.evaluate("""
                (element) => {
                    element.scrollBy({
                        top: 450, 
                        behavior: 'smooth'
                    })
                }
                """)
    
        print(f"Processing Lead {i+1} / {len(lead_buttons)}")
        
        await button.click(timeout=20000)
        print(f"Clicked on lead {i+1}")
        await human_delay(4, 5)
            
        right_panel_name = page.locator("div.project-name-location span.buyer_name")
        """Why the name right_panel_name? 
        Actually when you visit the leads section you will see 2 containers 
        The left contianer has like cards/buttons where leads are given in short. 
        When you click on one of those leads the in detail description of that lead is given in the 
        contianer to the right. 
        So here right_panel_name means name but from the contianer which is to the right of UI."""
        await right_panel_name.wait_for(state="visible", timeout=30000)
        await human_delay(1, 2)
        
        # Basic Info
        name = await right_panel_name.inner_text()
        print(name)
        category = await page.locator("div.project-title.strong").inner_text()
        location = (await page.locator("div.project-name-location span.location:visible").inner_text()).strip()
        print(location)
        
        # Unique ID
        lead_id = f"{name}-{location}"  
        
        # Check Database
        if lead_id in existing_ids:
            print(f"Skipping duplicate: {name}")
            print("\n" + "="*50)
            continue
        
        # Q&A details
        details_container = page.locator("div.project-questions-answers") 
        
        questions = await details_container.locator("div.project-details-question").all_inner_texts()
        answers = await details_container.locator("div.project-details-answer").all_inner_texts()                          
        
        details_dict = {}
        for q, a in zip(questions, answers):
            details_dict[q] = a
            
        # Budget extraction: We will use this in the next agent
        budget = details_dict.get("What is your estimated budget for this project?", "")
        
        # Create Lead Object
        lead_data = {
            "id": lead_id,
            "name": name, 
            "category": category, 
            "location": location,
            "budget": budget,
            "details": details_dict,
            "status": "NEW" 
        }
        
        # Save to JSON
        existing_leads.append(lead_data)
        save_leads(existing_leads)
        existing_ids.add(lead_id)
        
        new_leads_count += 1    
        print(f"Saved : {name} | {category} | {budget}")
        print("\n" + "="*50)
            
    print(f"Scraping finished. Total new leads added: {new_leads_count}")

    return {
        "next_action": "analyze"
    }  
    

                