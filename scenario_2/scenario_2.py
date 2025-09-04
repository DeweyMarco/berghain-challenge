import urllib.request
import json
import time
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
BASE_URL = os.getenv("BASE_URL")
# It's recommended to use a persistent player ID for tracking progress
PLAYER_ID = os.getenv("PLAYER_ID") # Replace with your actual player ID if you have one
SCENARIO = 2 # Scenario to run (1, 2, or 3)

RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # in seconds
VENUE_CAPACITY = 1000


class SimpleBouncer:
    """
    A concurrent constraint-optimization bouncer.
    
    Strategy:
    1. ALWAYS accept creative people (6.2% frequency, need all 300)
    2. CONCURRENTLY fill 700 non-creative slots while waiting for creatives:
       - Reserve 300 slots for creatives
       - Use remaining 700 slots for other attributes (berlin_local, techno_lover, etc.)
       - Prioritize people with multiple attributes for efficiency
       - Use urgency scoring when slots get scarce
    3. Key insight: Don't wait for creatives - optimize both streams simultaneously
    """
    
    def __init__(self, scenario, player_id, verbose=True):
        """
        Initialize the simple bouncer with game parameters.
        
        Args:
            scenario (int): The scenario number to play.
            player_id (str): The unique ID for the player.
            verbose (bool): Whether to enable verbose printing.
        """
        self.scenario = scenario
        self.player_id = player_id
        self.verbose = verbose
        self.game_id = None
        
        # Game constraints and tracking
        self.constraints = {}  # {"attribute": minCount}
        self.attribute_stats = {}  # Population statistics
        self.current_attribute_counts = {}  # Current counts of each attribute
        
        # Game state tracking
        self.admitted_count = 0
        self.rejected_count = 0
        

    def start_new_game(self):
        """
        Creates a new game and initializes the bouncer's state.
        
        Returns:
            Game data from the API, or None if there was an error
        """
        if self.verbose:
            print(f"Starting new game for scenario {self.scenario}...")
        url = f"{BASE_URL}/new-game?scenario={self.scenario}&playerId={self.player_id}"
        try:
            req = urllib.request.Request(url, method='POST')
            with urllib.request.urlopen(req) as response:
                if response.status < 200 or response.status >= 300:
                    raise urllib.error.HTTPError(url, response.status, response.reason, response.headers, response.fp)
                game_data = json.loads(response.read().decode('utf-8'))

            self.game_id = game_data['gameId']
            
            # Initialize constraints and statistics
            self.constraints = {c['attribute']: c['minCount'] for c in game_data['constraints']}
            self.attribute_stats = game_data['attributeStatistics']
            
            # Initialize current counts for each constrained attribute
            for attribute in self.constraints.keys():
                self.current_attribute_counts[attribute] = 0
            
            # Reset game state
            self.admitted_count = 0
            self.rejected_count = 0

            if self.verbose:
                print(f"Game {self.game_id} started.")
                print(f"Constraints: {self.constraints}")
                print(f"Attribute Statistics:")
                print(f"  Relative Frequencies: {self.attribute_stats['relativeFrequencies']}")
                if 'correlations' in self.attribute_stats:
                    print(f"  Correlations: {self.attribute_stats['correlations']}")
            return game_data
        except Exception as e:
            if self.verbose:
                print(f"Error starting game: {e}")
            return None

    def _get_next_person(self, person_index, accept=None):
        """
        Fetches the next person from the API, with retry logic for server errors.
        
        Args:
            person_index: Index of the current person
            accept: Whether we accepted (True) or rejected (False) the current person, or None for first person
            
        Returns:
            API response with next person data, or None if there was an error
        """
        url = f"{BASE_URL}/decide-and-next?gameId={self.game_id}&personIndex={person_index}"
        if accept is not None:
            url += f"&accept={str(accept).lower()}"
        
        # Retry logic: if we get a server error (5xx), wait and try again
        for attempt in range(RETRY_ATTEMPTS):
            try:
                req = urllib.request.Request(url, method='POST')
                with urllib.request.urlopen(req) as response:
                    if response.status < 200 or response.status >= 300:
                        raise urllib.error.HTTPError(url, response.status, response.reason, response.headers, response.fp)
                    return json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
                # Only retry on server errors (5xx), not client errors (4xx)
                if 500 <= e.code < 600 and attempt < RETRY_ATTEMPTS - 1:
                    if self.verbose:
                        print(f"Server error ({e.code}), retrying in {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY)
                else:
                    if self.verbose:
                        print(f"HTTP Error getting next person: {e}")
                    return None
            except Exception as e:
                if self.verbose:
                    print(f"Error getting next person: {e}")
                return None
        return None

    def _are_constraints_met(self):
        """Check if all constraints are satisfied."""
        for attribute, required_count in self.constraints.items():
            if self.current_attribute_counts.get(attribute, 0) < required_count:
                return False
        return True

    def _count_helpful_attributes(self, person_attributes):
        """Count how many constraints this person helps with."""
        count = 0
        for attribute, present in person_attributes.items():
            if present and attribute in self.constraints:
                needed = self.constraints[attribute] - self.current_attribute_counts.get(attribute, 0)
                if needed > 0:
                    count += 1
        return count
    
    def _can_still_meet_constraints(self):
        """Check if we can still meet all constraints with remaining capacity."""
        remaining_slots = VENUE_CAPACITY - self.admitted_count
        
        for attribute, required_count in self.constraints.items():
            needed = required_count - self.current_attribute_counts.get(attribute, 0)
            if needed > remaining_slots:
                return False
        return True

    def make_decision(self, person):
        """
        Strategy following SCENARIO2.md pseudocode:
        1. Always accept creative people
        2. For non-creatives with all 3 attributes (techno+well_connected+berlin):
           - Phase 1: Accept until well_connected = 450
           - Phase 2: Accept until techno_lover = 650  
           - Phase 3: Only accept if berlin_local + creative
        3. Once all constraints satisfied, accept everyone
        
        Returns: True to accept, False to reject
        """
        person_attributes = person['attributes']
        
        # Make the decision
        decision = self._make_decision_logic(person_attributes)
        
        
        return decision
    
    def _make_decision_logic(self, person_attributes):
        """Internal decision logic separated for cleaner data collection"""
        
        # Don't exceed venue capacity
        if self.admitted_count >= VENUE_CAPACITY:
            return False
        
        # ALWAYS accept creative people (rare 6.2%)
        if person_attributes.get('creative', False):
            return True
        
        # For non-creative people
        else:
            # Check if person has all three attributes: techno_lover + well_connected + berlin_local
            if (person_attributes.get('techno_lover', False) and 
                person_attributes.get('well_connected', False) and 
                person_attributes.get('berlin_local', False)):
                
                # Phase 1: Build well_connected constraint
                if self.current_attribute_counts.get('well_connected', 0) < 450:
                    return True
                
                # Phase 2: Build techno_lover constraint
                elif self.current_attribute_counts.get('techno_lover', 0) < 650:
                    return True
                
                # Phase 3: Both well_connected and techno_lover constraints met
                # Now focus on berlin_local and creative constraints
                else:
                    # Only accept if person has berlin_local AND creative
                    # (but we already know they're not creative, so reject)
                    return False
            
            # Phase 3 continued: Also check for berlin_local people (even if not techno+well_connected)
            # when we're in phase 3 (both well_connected and techno_lover constraints met)
            elif (self.current_attribute_counts.get('well_connected', 0) >= 450 and 
                  self.current_attribute_counts.get('techno_lover', 0) >= 650):
                # Accept if person has berlin_local (to help fill berlin_local constraint)
                if person_attributes.get('berlin_local', False):
                    return True
                else:
                    return False
            
            else:
                # Doesn't meet current criteria
                return False
        
        # Once all constraints are satisfied, accept everyone remaining
        if self._are_constraints_met():
            return True
        
        return False

    def run_game(self):
        """
        Runs the main game loop.
        
        The game flow is:
        1. Start a new game and get the first person
        2. For each person:
           - Make a decision (accept/reject)
           - Update our tracking variables
           - Get the next person
        3. Continue until the game ends (success, failure, or completion)
        """
        # Initialize the game
        if not self.start_new_game():
            return

        # Get the first person to start the loop
        result = self._get_next_person(person_index=0)
        if not result or not result.get('nextPerson'):
            print("Failed to get the first person.")
            return

        next_person = result.get('nextPerson')

        # Main game loop: process people until the game ends
        while result.get('status') == 'running' and next_person:
            # Make our decision for this person
            decision = self.make_decision(next_person)

            # Print person details and decision
            person_attrs = [attr for attr, present in next_person['attributes'].items() if present]
            fill_rate = (self.admitted_count / VENUE_CAPACITY) * 100
            if self.verbose:
                print(f"Person {next_person['personIndex']}: Attributes: {person_attrs}")
                print(f"  Venue {fill_rate:.1f}% full. Decision: {'Accept' if decision else 'Reject'}")

            # Send our decision to the API and get the next person
            result = self._get_next_person(person_index=next_person['personIndex'], accept=decision)

            if not result:
                if self.verbose:
                    print("Failed to get next person. Ending game.")
                break

            # Update our tracking variables
            if decision:
                self.admitted_count += 1
                for attr, present in next_person['attributes'].items():
                    if present and attr in self.current_attribute_counts:
                        self.current_attribute_counts[attr] += 1
                if self.verbose:
                    print(f"  -> Admitted. Counts: {self.current_attribute_counts}")
            else:
                self.rejected_count += 1
                if self.verbose:
                    print(f"  -> Rejected.")

            # Get the next person for the next iteration
            next_person = result.get('nextPerson')

            # Small delay to avoid overwhelming the API
            time.sleep(0.05)

        # Game has ended - show final results
        if result and result.get('status') == 'completed':
            
            if self.verbose:
                print("--- GAME COMPLETED ---")
                print(f"Final Admitted: {self.admitted_count}")
                print(f"Final Rejected: {result['rejectedCount']}")
                print(f"Final Constraint Status:")
                for attr, required in self.constraints.items():
                    current = self.current_attribute_counts.get(attr, 0)
                    status = "✓" if current >= required else f"✗ ({current}/{required})"
                    print(f"  {attr}: {status}")
                print("----------------------")
        elif result and result.get('status') == 'failed':
            
            if self.verbose:
                print("--- GAME FAILED ---")
                print(f"Reason: {result.get('reason')}")
                print(f"Final Admitted: {self.admitted_count}")
                print(f"Final Rejected: {self.rejected_count}")
                print(f"Final Constraint Status:")
                for attr, required in self.constraints.items():
                    current = self.current_attribute_counts.get(attr, 0)
                    status = "✓" if current >= required else f"✗ ({current}/{required})"
                    print(f"  {attr}: {status}")
                print("---------------------")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Berghain Challenge Scenario 2')
    parser.add_argument('--quiet', '-q', action='store_true', 
                       help='Disable verbose output (only show minimal information)')
    args = parser.parse_args()
    
    # Create an instance of our bouncer with verbose setting
    verbose = not args.quiet
    bouncer = SimpleBouncer(scenario=SCENARIO, player_id=PLAYER_ID, verbose=verbose)
    bouncer.run_game()