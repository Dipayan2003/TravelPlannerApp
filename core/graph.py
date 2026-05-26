from langgraph.graph import StateGraph, START, END
from core.state import TravelPlanState

# Import all our custom agent nodes
from agents.router_agent import router_node
from agents.researcher_agent import researcher_node
from agents.transport_agent import transport_node
from agents.hotel_agent import hotel_node
from agents.itinerary_agent import itinerary_node
from agents.final_response_agent import final_response_node

def create_travel_graph():
    # 1. Initialize the StateGraph with our blueprint notebook structure
    workflow = StateGraph(TravelPlanState)
    
    # 2. Register each agent function as a structural node in the network
    workflow.add_node("router", router_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("transport", transport_node)
    workflow.add_node("hotel", hotel_node)
    workflow.add_node("itinerary", itinerary_node)
    workflow.add_node("final_response", final_response_node)
    
    # 3. Define the structural pipeline using directed edges
    # The START node triggers the Router Agent first
    workflow.add_edge(START, "router")
    
    # Sequential processing chain: The data builds up at each step
    workflow.add_edge("router", "researcher")
    workflow.add_edge("researcher", "transport")
    workflow.add_edge("transport", "hotel")
    workflow.add_edge("hotel", "itinerary")
    workflow.add_edge("itinerary", "final_response")
    
    # Once the Cost Analysis finishes, point to the absolute END of the graph lifecycle
    workflow.add_edge("final_response", END)
    
    # 4. Compile the graph configuration into an executable application state
    return workflow.compile()