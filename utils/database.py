import os
import json

DB_FILE = "data/leads.json"

def load_existing_leads():
    if not os.path.exists(DB_FILE):
        return []
    else: 
        with open(DB_FILE, "r") as f:
            return json.load(f)
        
def save_leads(leads):
    os.makedirs("data", exist_ok=True)
    with open(DB_FILE, "w") as f:
        json.dump(leads, f, indent=2)