from core.state import TravelPlanState
from tools.api_tools import search_flights, search_ground_transport

def transport_node(state: TravelPlanState) -> dict:
    print("--- TRANSPORT AGENT: Determining transit options ---")
    
    # Extract variables currently stored in the graph state
    origin = state.get("origin")
    destination = state.get("destination")
    start_date = state.get("start_date")
    travel_type = state.get("travel_type")
    
    options = []
    
    # Execution Logic: Separate paths based on Router Agent's decision
    if travel_type == "international":
        print("-> Directing to Flight Search Sub-System")
        options = search_flights(origin, destination, start_date)
    else:
        print("-> Directing to Ground (Train/Bus) Search Sub-System")
        options = search_ground_transport(origin, destination, start_date)
    
    print(f"--- TRANSPORT AGENT: Found {len(options)} transit matching paths ---")
    
    # Return a dictionary targeting 'transport_options'. 
    # Because 'transport_options' is Annotated with 'add' in state.py, 
    # LangGraph will automatically append this list to any existing ones instead of wiping it.
    return {"transport_options": options}