# def main():
#     print("Hello from travelplannerapp!")


# if __name__ == "__main__":
#     main()
from dotenv import load_dotenv
from core.graph import create_travel_graph

# Explicitly load local environment variable settings
load_dotenv()

def run_test_pipeline():
    print("=============================================")
    print("INITIALIZING MULTI-AGENT TRAVEL PLANNING SYSTEM")
    print("=============================================\n")
    
    # Compile the graph architecture
    app = create_travel_graph()
    
    # Define an initial query state representing user configuration choices
    # Test case 1 (International flight parsing query)
    initial_inputs = {
        "origin": "Kolkata",            # Airport code for flight tool processing
        "destination": "Kashmir",
        "start_date": "2026-07-10",
        "end_date": "2026-07-17"
    }
    
    print(f"Planning trip from '{initial_inputs['origin']}' to '{initial_inputs['destination']}'...\n")
    
    # Run the graph application synchronously by passing the entry parameters
    final_output_state = app.invoke(initial_inputs)
    
    print("\n=============================================")
    print("           FINAL AGENT OUTPUT REPORT         ")
    print("=============================================\n")
    
    # Retrieve and output the detailed combined analysis generated at the final node
    if "total_cost_estimate" in final_output_state:
        print(final_output_state["total_cost_estimate"])
    else:
        print("Error: The multi-agent graph failed to compile a final response.")

if __name__ == "__main__":
    run_test_pipeline()