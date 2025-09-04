import json
import urllib.request
import io
import importlib
import time
import sys
import os
import inspect
import argparse

# Import the simulation engine
from simulation_engine import SimulationEngine

# --- Simulation Configurations ---
SCENARIO_1_CONFIG = {
    "constraints": {
        "young": 600,
        "well_dressed": 600
    },
    "venue_capacity": 1000
}

SCENARIO_2_CONFIG = {
    "constraints": {
        "techno_lover": 650,
        "well_connected": 450,
        "creative": 300,
        "berlin_local": 750
    },
    "venue_capacity": 1000
}

SCENARIO_3_CONFIG = {
    "constraints": {
        "underground_veteran": 500,
        "international": 650,
        "fashion_forward": 550,
        "queer_friendly": 250,
        "vinyl_collector": 200,
        "german_speaker": 800
    },
    "venue_capacity": 1000
}

# --- Monkey-Patching Setup ---

# Store the original urlopen function so we can restore it later
original_urlopen = urllib.request.urlopen

def create_mock_handler(simulation):
    """Creates a mock urlopen function that intercepts network calls and redirects them to the simulation."""
    
    class MockHTTPResponse:
        """A mock HTTPResponse object that mimics the behavior of a real one for the bouncer scripts."""
        def __init__(self, data):
            self._stream = io.BytesIO(json.dumps(data).encode('utf-8'))
            self.status = 200
            self.reason = "OK"
            # The bouncer scripts use a context manager (`with ... as response:`), which requires these methods.
            self.fp = self._stream

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def getheaders(self):
            return {'Content-Type': 'application/json'}

        def read(self, *args, **kwargs):
            return self._stream.read(*args, **kwargs)

    def mock_urlopen(request, *args, **kwargs):
        """The function that will replace urllib.request.urlopen."""
        url = request.get_full_url()
        # print(f"[SIM] Intercepted request to: {url}") # Uncomment for verbose logging

        response_data = {}
        
        # Route the request to the correct simulation method based on the URL
        if "/new-game" in url:
            response_data = simulation.start_game()
        elif "/decide-and-next" in url:
            # Extract the bouncer's decision from the URL query parameters
            decision = None
            if "accept=true" in url:
                decision = True
            elif "accept=false" in url:
                decision = False
            response_data = simulation.decide_and_next(decision)
        else:
            # If the URL is not one we're mocking, raise an error
            raise ValueError(f"Unhandled mock URL: {url}")

        return MockHTTPResponse(response_data)
        
    return mock_urlopen

def run_simulation_with_bouncer(bouncer_class, scenario_config, scenario_number, verbose=True):
    """
    Sets up and runs a local simulation for a given bouncer class.
    """
    if verbose:
        print(f"\n--- Running scenario {scenario_number} simulation for: {bouncer_class.__name__} ---")
    
    # 1. Initialize the simulation engine
    simulation = SimulationEngine(scenario_config, scenario_number)
    
    # 2. Create the mock urlopen function and apply the monkey-patch
    mock_handler = create_mock_handler(simulation)
    urllib.request.urlopen = mock_handler
    
    # 3. Temporarily modify the bouncer's target URL to prevent any accidental real requests.
    # This is a safety measure; the patch should catch all relevant calls.
    bouncer_module = importlib.import_module(bouncer_class.__module__)
    original_base_url = bouncer_module.BASE_URL
    bouncer_module.BASE_URL = "http://localhost.mock"
    # Reduce sleep time to speed up simulation
    original_sleep_time = time.sleep
    time.sleep = lambda x: None 

    # 4. Instantiate and run the bouncer. Its network calls will now be handled by our simulator.
    bouncer = bouncer_class(scenario=scenario_number, player_id="local-player", verbose=verbose)
    
    try:
        bouncer.run_game()
    except Exception as e:
        print(f"An error occurred during simulation for {bouncer_class.__name__}: {e}")
    finally:
        # Print final simulation statistics
        print(f"\\n--- Final Statistics for {bouncer_class.__name__} ---")
        print(f"Total people admitted: {simulation.admitted_count}")
        print(f"Total people rejected: {simulation.rejected_count}")
        print(f"Current attribute counts: {simulation.current_attribute_counts}")
        print(f"Required constraints: {simulation.config['constraints']}")
        
        # Calculate and print success rates for each constraint
        print("\\n--- Constraint Achievement ---")
        for attr, required in simulation.config['constraints'].items():
            actual = simulation.current_attribute_counts[attr]
            percentage = (actual / required * 100) if required > 0 else 0
            status = "✓" if actual >= required else "✗"
            print(f"{status} {attr}: {actual}/{required} ({percentage:.1f}%)")
        # 5. Clean up: Restore the original urlopen, BASE_URL, and sleep function
        urllib.request.urlopen = original_urlopen
        bouncer_module.BASE_URL = original_base_url
        time.sleep = original_sleep_time
        if verbose:
            print(f"--- Scenario {scenario_number} simulation for {bouncer_class.__name__} finished. Restored network functions. ---")


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Berghain Challenge Local Simulation')
    parser.add_argument('scenario_number', type=int, choices=[1, 2, 3],
                       help='The scenario number to run (1, 2, or 3)')
    parser.add_argument('bouncer_script_path', type=str,
                       help='Path to the bouncer script (e.g., scenario_1/scenario_1.py)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Disable verbose output (only show minimal information)')
    args = parser.parse_args()

    scenario_number = args.scenario_number
    bouncer_script_path = args.bouncer_script_path
    verbose = not args.quiet
    
    if not os.path.exists(bouncer_script_path):
        print(f"Error: File not found at {bouncer_script_path}")
        sys.exit(1)

    # Convert file path to module name for import
    module_name = os.path.splitext(bouncer_script_path)[0].replace('/', '.')

    try:
        # Dynamically import the specified module
        bouncer_module = importlib.import_module(module_name)
    except ImportError as e:
        print(f"Error importing module {module_name}: {e}")
        sys.exit(1)

    # Find the bouncer class within the module
    # We assume the target class is the one defined within that file.
    # Use the last class found to avoid utility classes like APIDataCollector
    bouncer_class = None
    for name, obj in inspect.getmembers(bouncer_module):
        if inspect.isclass(obj) and obj.__module__ == bouncer_module.__name__:
            bouncer_class = obj
            # Don't break - continue to find the last (main) class

    if bouncer_class:
        # Select the appropriate scenario configuration
        scenario_configs = {
            1: SCENARIO_1_CONFIG,
            2: SCENARIO_2_CONFIG,
            3: SCENARIO_3_CONFIG
        }
        selected_config = scenario_configs[scenario_number]
        
        # Run the simulation with the dynamically loaded bouncer
        run_simulation_with_bouncer(bouncer_class, selected_config, scenario_number, verbose)
    else:
        print(f"Could not find a bouncer class defined in {bouncer_script_path}")
        sys.exit(1)