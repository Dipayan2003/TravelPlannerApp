from typing import TypedDict, List, Dict, Any, Annotated
from operator import add

# The State defines all the variables our agents will share and update.
class TravelPlanState(TypedDict):
    origin: str
    destination: str
    start_date: str
    end_date: str
    
    # Routing decision: "domestic" or "international"
    travel_type: str 
    
    # Annotated with 'add' means if multiple agents append data, it creates a list 
    # rather than overwriting the previous data.
    transport_options: Annotated[List[Dict[str, Any]], add]
    hotel_options: Annotated[List[Dict[str, Any]], add]
    
    # Research from travel blogs (Tavily)
    tourist_spots: str
    
    # The final compiled response
    final_itinerary: str
    total_cost_estimate: str