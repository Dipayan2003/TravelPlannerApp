from langchain_core.prompts import ChatPromptTemplate
from core.state import TravelPlanState
from core.llm import get_llm
from tools.api_tools import search_travel_blogs

def researcher_node(state: TravelPlanState) -> dict:
    print("--- RESEARCHER AGENT: Gathering destination intel ---")
    
    destination = state.get("destination")
    travel_type = state.get("travel_type")
    
    # 1. Call our custom tool to get raw scraped data from the internet
    raw_research = search_travel_blogs(destination, travel_type)
    
    # 2. Initialize Llama 3 to synthesize the messy web data
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert travel researcher. Your job is to read raw search results from travel blogs and extract the best places to visit. "
                   "Format your response cleanly. Include a section for 'Must-See Popular Spots' and a section for 'Underrated Hidden Gems'."),
        ("human", "Destination: {destination}\n\nRaw Search Data:\n{raw_data}")
    ])
    
    # Create the chain
    chain = prompt | llm
    
    # Invoke Llama 3 with the raw data
    result = chain.invoke({
        "destination": destination,
        "raw_data": raw_research
    })
    
    print("--- RESEARCHER AGENT: Intel synthesized ---")
    
    # 3. Return the synthesized text to update the 'tourist_spots' variable in our State notebook
    return {"tourist_spots": result.content}