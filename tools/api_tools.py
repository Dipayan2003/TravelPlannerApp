import os
import requests
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# --- Initialize API Keys ---
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# --- 1. Research Tool (Tavily) ---
def search_travel_blogs(destination: str, travel_type: str) -> str:
    """Searches the web for travel blogs to find popular and hidden gem locations."""
    query = f"best travel blogs itinerary for {destination} popular tourist spots and underrated hidden gems"
    if travel_type == "international":
        query += " international travel tips customs"
        
    print(f"--- TAVILY SEARCHING: {query} ---")
    
    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=3
        )
        
        results = []
        for result in response.get("results", []):
            results.append(f"Source: {result['url']}\nContent: {result['content']}\n")
            
        return "\n".join(results)
    except Exception as e:
        print(f"Tavily Search Error: {e}")
        return "Could not retrieve travel blog data."

# --- 2. Flight Tool (AviationStack) ---
def search_flights(origin: str, destination: str, date: str) -> list:
    """Queries the AviationStack API for flight routes matching the criteria."""
    print(f"--- API TOOL: Fetching flights from {origin} to {destination} ---")
    
    url = "http://api.aviationstack.com/v1/routes"
    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "dep_iata": origin.strip().upper()[:3],
        "arr_iata": destination.strip().upper()[:3]
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            flights = data.get("data", [])
            
            if not flights:
                return [
                    {"type": "Flight", "provider": "Global Airways", "route": f"{origin} -> {destination}", "cost": 650, "duration": "8h 30m"},
                    {"type": "Flight", "provider": "EcoFly", "route": f"{origin} -> {destination}", "cost": 520, "duration": "9h 15m"}
                ]
            
            parsed_flights = []
            for item in flights[:3]:
                parsed_flights.append({
                    "type": "Flight",
                    "provider": item.get("airline_name", "Commercial Carrier"),
                    "route": f"{item.get('departure_airport')} -> {item.get('arrival_airport')}",
                    "cost": 600, 
                    "duration": "Variable"
                })
            return parsed_flights
        else:
            print(f"AviationStack API Error: Status {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to AviationStack: {e}")
        
    return [{"type": "Flight", "provider": "Standard Carrier", "route": f"{origin} -> {destination}", "cost": 550, "duration": "Direct"}]

# --- 3. Ground Transport Tool (Simulation) ---
def search_ground_transport(origin: str, destination: str, date: str) -> list:
    """Simulates a domestic train and bus aggregation engine API lookup."""
    print(f"--- API TOOL: Fetching trains and buses from {origin} to {destination} ---")
    
    return [
        {
            "type": "Train",
            "provider": "National Rail Express",
            "route": f"{origin} Central -> {destination} Terminal",
            "cost": 45,
            "duration": "3h 15m"
        },
        {
            "type": "Bus",
            "provider": "InterCity Liner",
            "route": f"{origin} Bus Stop A -> {destination} Plaza",
            "cost": 25,
            "duration": "5h 00m"
        }
    ]

# --- 4. Hotel Search Tool (Simulation) ---
def search_hotels(destination: str, travel_type: str) -> list:
    """Simulates querying a hotel booking API for accommodations."""
    print(f"--- API TOOL: Fetching hotels for {destination} ---")
    
    # In a real system, you would pass dates and use an API like SerpApi or Amadeus.
    # We adjust the price tier slightly based on international vs domestic.
    base_multiplier = 1.5 if travel_type == "international" else 1.0
    
    return [
        {
            "name": f"Grand {destination} Plaza",
            "type": "Luxury Hotel",
            "rating": "4.8/5",
            "price_per_night": int(200 * base_multiplier),
            "amenities": "Pool, Spa, Free Breakfast"
        },
        {
            "name": f"{destination} Central Inn",
            "type": "Boutique Hotel",
            "rating": "4.2/5",
            "price_per_night": int(95 * base_multiplier),
            "amenities": "City View, Gym, Fast Wi-Fi"
        },
        {
            "name": f"Backpackers Haven {destination}",
            "type": "Hostel",
            "rating": "4.5/5",
            "price_per_night": int(30 * base_multiplier),
            "amenities": "Shared Kitchen, Social Lounge, Bar"
        }
    ]