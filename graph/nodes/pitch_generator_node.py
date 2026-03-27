from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from graph.states import *
from graph.prompts import *
from utils.database import *
from utils.helpers import *

llm = ChatGroq(model="openai/gpt-oss-120b", max_tokens=16384)

async def pitch_generator_node(state: AgentState) -> dict:
    print(" ---NODE: PITCH GENERATOR---")
    
    # Load all leads from DB
    all_leads = load_existing_leads()
    
    # Filter for High Quality Leads that haven't been pitched yet
    # Criteria: Status is ANALYZED and score >= 0.8
    qualified_leads = [
        lead for lead in all_leads
        if lead.get('status') == "ANALYZED" and lead.get('score', 0) >= 0.8
    ]
    
    if not qualified_leads:
        print("No high quality leads found for pitching.")
        return {'next_action': 'end'}
    
    print(f"Found {len(qualified_leads)} leads to pitch.")
    
    pitched_leads = []
    # Generate pitches
    for lead in qualified_leads:
        print(f"Writing pitch for: {lead['id']}")
        
        # Prepare details string 
        details_text = json.dumps(lead.get('details', {}), indent=2)
        
        # Create prompt 
        prompt = ChatPromptTemplate.from_messages([
            ('system', PITCH_PROMPT),
            ('human', CLIENT_DETAILS)
        ])
        
        chain = prompt | llm | StrOutputParser()
        
        pitch = await chain.ainvoke({
            "name": lead['name'], 
            "budget": lead['budget'],
            "details": details_text 
        })
        
        # Update lead
        lead['pitch'] = pitch
        lead['status'] = "PITCHED"
        
        pitched_leads.append(lead)
        
        # Small delay so that we dont overwhelm the llm
        await human_delay(4, 5)
        print(f"✅ Pitch generated for {lead['id']}")
    
    leads_map = {lead['id']: lead for lead in all_leads}
    
    for pitched_lead in pitched_leads:
        if pitched_lead['id'] in leads_map:
            leads_map[pitched_lead['id']] = pitched_lead 
            
    save_leads(list(leads_map.values()))
    
    return {'next_action' : 'end'}