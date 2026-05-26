from langchain_core.prompts import ChatPromptTemplate
from core.state import TravelPlanState
from core.llm import get_llm

def itinerary_node(state: TravelPlanState) -> dict:
    print("--- ITINERARY AGENT: Crafting day-by-day schedule ---")
    
    # 1. Fetch our high-reasoning engine (Llama 3.3 70B via Groq)
    llm = get_llm()
    
    # 2. Build the system prompt instructing it to merge the timeline with our research
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an elite travel concierge. Your job is to draft a realistic, day-by-day trip itinerary "
                   "based on the user's destination, dates, and the synthesized travel blog data provided. "
                   "Ensure you incorporate both popular highlights and hidden gems. "
                   "Be detailed, creative, and structured. Do not include cost info yet; focus purely on the schedule."),
        ("human", "Destination: {destination}\nDates: {start_date} to {end_date}\n\n"
                   "Recommended Spots from Blogs:\n{tourist_spots}")
    ])
    
    chain = prompt | llm
    
    # 3. Invoke the LLM using our graph's state variables
    result = chain.invoke({
        "destination": state.get("destination"),
        "start_date": state.get("start_date"),
        "end_date": state.get("end_date"),
        "tourist_spots": state.get("tourist_spots")
    })
    
    print("--- ITINERARY AGENT: Day-by-day schedule finalized ---")
    
    # Update the final_itinerary tracker in our state
    return {"final_itinerary": result.content}