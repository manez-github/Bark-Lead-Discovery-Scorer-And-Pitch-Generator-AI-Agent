from graph.graph import *

async def run_agent_loop():
    """
    Runs the agent continuously with some time intervals in between.
    Constantly looks for new leads.
    """
    
    while True:
        print("\n" + "="*50)
        print('STARTING NEW AGENT CYCLE')
        print("\n" + "="*50 + "\n")
        
        await run_graph()
        
        wait_hours = 6
        wait_seconds = wait_hours * 60 * 60
        print(f"\nCycle complete. Sleeping for {wait_hours} hours.")
        await asyncio.sleep(wait_seconds)
        
if __name__ == "__main__":
    keep_awake()   # Does not let pc sleep while the code is getting executed.
    
    try:
        asyncio.run(run_agent_loop())
    except KeyboardInterrupt:
        print("\nAgent stopped manually.")