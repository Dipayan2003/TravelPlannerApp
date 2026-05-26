from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from core.state import TravelPlanState
from core.llm import get_llm

# 1. Define the exact structure we want the LLM to output
class RouteDecision(BaseModel):
    travel_type: str = Field(
        description="Must be 'domestic' if both origin and destination are in the same country. Must be 'international' if they are in different countries."
    )

# 2. Define the node function for LangGraph
def router_node(state: TravelPlanState) -> dict:
    print("--- ROUTER AGENT: Analyzing locations ---")
    
    # Fetch our Groq Llama 3 model
    llm = get_llm()
    
    # Bind the Pydantic schema to the LLM to force JSON/Structured output
    structured_llm = llm.with_structured_output(RouteDecision)
    
    # Create a focused prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert geographical router for an AI travel planning system. "
                   "Your only job is to determine if a trip is 'domestic' or 'international'."),
        ("human", "Origin: {origin}\nDestination: {destination}")
    ])
    
    # Create the chain: Prompt -> LLM
    chain = prompt | structured_llm
    
    # Invoke the chain using the data currently sitting in the LangGraph state
    result = chain.invoke({
        "origin": state.get("origin"), 
        "destination": state.get("destination")
    })
    
    print(f"--- ROUTER AGENT DECISION: {result.travel_type.upper()} ---")
    
    # Return a dictionary with the key(s) we want to update in our TravelPlanState
    return {"travel_type": result.travel_type}