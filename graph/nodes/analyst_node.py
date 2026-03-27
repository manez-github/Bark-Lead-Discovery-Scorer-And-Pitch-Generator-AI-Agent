import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from graph.states import *
from graph.prompts import *
from utils.helpers import *
from utils.database import *

llm = ChatGroq(model="openai/gpt-oss-120b", max_tokens=16384)

structured_llm = llm.with_structured_output(LeadScore)

async def analyst_node(state: AgentState) -> dict:
    print("NODE: --- ANALYST ---")
    
    # Load current DB
    existing_data = load_existing_leads()
    
    leads = [lead for lead in existing_data if lead.get('status') == "NEW"]
    
    if not leads:
        print("No leads to analyze")
        return {"next_action": "end"}
    
    analyzed_leads = []
    
    for lead in leads:
        print(f"Analyzing lead: {lead['id']}...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", ICP_DESCRIPTION), 
            ("human", "Lead Details:\n{lead_details}")
        ])
        
        # Convert leads that are in json format in text format and give it to llms
        details_text = f"""
        Name: {lead['name']}
        Location: {lead['location']}
        Budget: {lead['budget']}
        Category: {lead['category']}
        Full Details: {json.dumps(lead['details'], indent=2)}"""
        
        # Create the chain:
        chain = prompt | structured_llm
        
        # Invoke llm
        result = await chain.ainvoke({"lead_details": details_text})
        
        # Update the lead object with AI results
        lead['score'] = result.score
        lead['reasoning'] = result.reasoning
        lead['is_qualified'] = result.is_qualified
        lead['status'] = "ANALYZED"
        
        print(f"Score: {result.score} | Qualified: {result.is_qualified}")
        
        analyzed_leads.append(lead)
        
        # Small delay so that we dont overwhelm the llm
        await human_delay(4, 5)
        
    # Update JSON database    
    existing_map = {lead['id']: lead for lead in existing_data}
    
    for new_lead in analyzed_leads:
        if new_lead['id'] in existing_map:
            existing_map[new_lead['id']] = new_lead
            
    save_leads(list(existing_map.values()))
    
    return {'next_action': 'pitch'}