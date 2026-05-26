from langchain_core.prompts import ChatPromptTemplate
from core.state import TravelPlanState
from core.llm import get_llm

def final_response_node(state: TravelPlanState) -> dict:
    print("--- COST ANALYSIS AGENT: Calculating final breakdown ---")
    
    llm = get_llm()
    
    # Convert lists of transport and hotel dicts to clean strings so the LLM can parse them easily
    transport_str = "\n".join([f"- {t['type']} via {t['provider']} ({t['route']}): ${t['cost']} [Duration: {t['duration']}]" for t in state.get("transport_options", [])])
    hotel_str = "\n".join([f"- {h['name']} ({h['type']}): ${h['price_per_night']}/night, Rating: {h['rating']}, Amenities: {h['amenities']}" for h in state.get("hotel_options", [])])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert travel financial analyst and summary coordinator. "
                   "Your job is to take a draft itinerary, a list of flight/ground transport options, and hotel options, "
                   "and produce a comprehensive, final travel report. "
                   "Your output must include:\n"
                   "1. The comprehensive Day-by-Day Itinerary.\n"
                   "2. A dedicated 'Transportation and Stay Options' breakdown.\n"
                   "3. A 'Cost Analysis & Estimated Total Budget' calculating an estimated baseline expense based on choices.\n"
                   "Keep it looking clean, highly professional, and easy to read."),
        ("human", "Draft Schedule:\n{itinerary}\n\nAvailable Transport:\n{transport}\n\nAvailable Hotels:\n{hotels}")
    ])
    
    chain = prompt | llm
    
    result = chain.invoke({
        "itinerary": state.get("final_itinerary"),
        "transport": transport_str,
        "hotels": hotel_str
    })
    
    print("--- COST ANALYSIS AGENT: Compilation complete ---")
    
    return {"total_cost_estimate": result.content}