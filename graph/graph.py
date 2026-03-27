import asyncio
from langgraph.graph import StateGraph, END

from graph.states import *
from graph.nodes.init_node import *
from graph.nodes.auth_check_node import *
from graph.nodes.login_node import *
from graph.nodes.scraper_node import *
from graph.nodes.analyst_node import *
from graph.nodes.pitch_generator_node import *
from graph.nodes.close_node import *

def route_next_action(state: AgentState) -> str:
    return state['next_action']

async def run_graph():
    print("Starting Graph")
    
    graph = StateGraph(AgentState)
    
    graph.add_node("init", init_node)
    graph.add_node("auth_check", auth_check_node)
    graph.add_node("login", login_node)
    graph.add_node("scraper", scraper_node)
    graph.add_node("analyst", analyst_node)
    graph.add_node("pitcher", pitch_generator_node)
    graph.add_node("close", close_node)
    
    graph.set_entry_point("init")

    graph.add_edge("init", "auth_check")
    graph.add_conditional_edges(
        "auth_check", 
        route_next_action, 
        {
            "login": "login", 
            "scrape": "scraper"
        }
    )
    graph.add_edge("login", "auth_check")
    graph.add_edge("scraper", "analyst")
    graph.add_conditional_edges(
        "analyst",
        route_next_action,
        {
            "pitch": "pitcher",
            "end": "close"
        }
    )
    graph.add_edge("pitcher", "close")
    graph.add_edge("close", END)
    
    agent = graph.compile()
    
    initial_state = {}
    
    async for event in agent.astream(initial_state):
        for node_name, node_output in event.items():
            print(f"✅ NODE FINISHED: {node_name}")
            print(f"    OUTPUT KEYS: {node_output.keys()}")
    
    print("Bark AI Agent Execution finished")

if __name__ == "__main__":
    keep_awake()   # Does not let pc sleep while the code is getting executed.
    asyncio.run(run_graph())