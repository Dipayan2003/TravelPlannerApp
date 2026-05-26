from core.state import TravelPlanState
from tools.api_tools import search_hotels

def hotel_node(state: TravelPlanState) -> dict:
    print("--- HOTEL AGENT: Searching for accommodations ---")
    
    # Extract needed variables from the state
    destination = state.get("destination")
    travel_type = state.get("travel_type")
    
    # Execute the tool
    hotel_results = search_hotels(destination, travel_type)
    
    print(f"--- HOTEL AGENT: Found {len(hotel_results)} accommodation options ---")
    
    # Return a dictionary targeting 'hotel_options'.
    # Because it is Annotated with 'add' in our state, this safely appends the list.
    return {"hotel_options": hotel_results}