import urllib.request
import json
import time
import os
import argparse
from dotenv import load_dotenv

# Load environment variables from a .env file for configuration
load_dotenv()

# --- Configuration ---
# The base URL of the game API server
BASE_URL = os.getenv("BASE_URL")
# A unique identifier for the player. Using a consistent ID allows tracking progress across games.
PLAYER_ID = os.getenv("PLAYER_ID") 
# The specific scenario to run (e.g., 1, 2, or 3)
SCENARIO = 1

# --- Game Settings ---
# Number of times to retry a request if the server fails
RETRY_ATTEMPTS = 3
# Delay in seconds between retries
RETRY_DELAY = 1
# The total capacity of the venue
VENUE_CAPACITY = 1000


class AdaptiveBouncer:
    """
    A bouncer specifically for Scenario 1, following the user's strategy.

    The algorithm works in three phases:
    1. First 1,200 people: Accept everyone with at least one attribute, reject those with neither
    2. After 1,200 people: Dynamically accept people with neither attributes to minimize rejections
       until all constraints are satisfied
    3. Once constraints are met: Accept everyone to fill the venue
    """
    
    def __init__(self, scenario, player_id, verbose=True):
        """
        Initializes the bouncer's state for a new game.
        
        Args:
            scenario (int): The scenario number to play.
            player_id (str): The unique ID for the player.
            verbose (bool): Whether to enable verbose printing.
        """
        self.scenario = scenario
        self.player_id = player_id
        self.verbose = verbose
        self.game_id = None  # Will be set when a new game starts
        self.constraints = {}  # Stores the minimum required counts for each attribute
        self.attribute_stats = {}  # Stores statistics about attribute frequencies
        self.current_attribute_counts = {}  # Tracks the number of admitted people for each attribute
        self.admitted_count = 0  # Total number of people admitted
        self.rejected_count = 0  # Total number of people rejected
        
        
        # --- Correlation Tracking for Simulation Improvement ---
        self.people_seen = 0  # Total people observed
        self.combination_counts = {
            'young_only': 0,
            'well_dressed_only': 0, 
            'both_young_well_dressed': 0,
            'neither': 0
        }
        
        # --- Strategy Thresholds ---
        # The number of people to process in the first phase of the strategy
        self.phase1_threshold = 1200
        # Base threshold for a dynamic scoring model (currently unused in this strategy)
        self.base_threshold = 0.7
        # Fill rate threshold to switch to a more lenient phase (currently unused)
        self.phase2_threshold = 0.9

    def start_new_game(self):
        """
        Starts a new game by making a POST request to the API.
        
        Initializes the game state, including the game ID, constraints, and attribute counts.
        
        Returns:
            dict: The game data from the API if successful, otherwise None.
        """
        if self.verbose:
            print(f"Starting new game for scenario {self.scenario}...")
        url = f"{BASE_URL}/new-game?scenario={self.scenario}&playerId={self.player_id}"
        try:
            # Make a POST request to the /new-game endpoint
            req = urllib.request.Request(url, method='POST')
            with urllib.request.urlopen(req) as response:
                # Check for a successful HTTP status code
                if response.status < 200 or response.status >= 300:
                    raise urllib.error.HTTPError(url, response.status, response.reason, response.headers, response.fp)
                game_data = json.loads(response.read().decode('utf-8'))

            # --- Initialize Game State ---
            self.game_id = game_data['gameId']
            # Convert the list of constraints into a more accessible dictionary
            self.constraints = {c['attribute']: c['minCount'] for c in game_data['constraints']}
            self.attribute_stats = game_data['attributeStatistics']
            
            # Initialize the counts for each required attribute to zero
            for attribute in self.constraints.keys():
                self.current_attribute_counts[attribute] = 0
            
            # Reset admission and rejection counters
            self.admitted_count = 0
            self.rejected_count = 0
            self.neither_count = 0
            
            # Reset correlation tracking
            self.people_seen = 0
            self.combination_counts = {
                'young_only': 0,
                'well_dressed_only': 0,
                'both_young_well_dressed': 0,
                'neither': 0
            }

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
        Fetches the next person from the API and submits the decision for the current person.
        
        Includes retry logic for handling transient server errors (5xx).
        
        Args:
            person_index (int): The index of the current person being decided upon.
            accept (bool, optional): The decision for the current person (True for accept, False for reject).
                                     None for the very first request.
            
        Returns:
            dict: The API response containing the next person's data, or None if an error occurs.
        """
        # Construct the API endpoint URL with query parameters
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
                # Only retry on server-side errors (5xx), not client-side errors (4xx)
                if 500 <= e.code < 600 and attempt < RETRY_ATTEMPTS - 1:
                    if self.verbose:
                        print(f"Server error ({e.code}), retrying in {RETRY_DELAY}s...")
                    time.sleep(RETRY_DELAY)
                else:
                    # For persistent errors or client errors, log and fail
                    if self.verbose:
                        print(f"HTTP Error getting next person: {e}")
                    return None
            except Exception as e:
                if self.verbose:
                    print(f"Error getting next person: {e}")
                return None
        return None

    def _calculate_constraint_score(self, person_attributes):
        """
        NOTE: This method is part of a more complex scoring strategy and is NOT USED in the current simplified logic.
        
        Calculates how much this person helps satisfy unfulfilled constraints.
        The score is based on how urgently an attribute is needed and how rare it is.
        
        Args:
            person_attributes (dict): A dictionary mapping attribute names to boolean presence.
            
        Returns:
            float: A numeric score representing the person's value in satisfying constraints.
        """
        score = 0
        
        for attribute, present in person_attributes.items():
            # Skip if the person doesn't have this attribute or if it's not a required constraint
            if not present or attribute not in self.constraints:
                continue

            # Calculate how many more people with this attribute are needed
            needed_count = self.constraints[attribute] - self.current_attribute_counts[attribute]
            
            # If we've already met the constraint for this attribute, it adds no value
            if needed_count <= 0:
                continue

            # Get the frequency of this attribute in the general population (defaults to a small number to avoid division by zero)
            frequency = self.attribute_stats['relativeFrequencies'].get(attribute, 0.001)
            
            # Rarity is the inverse of frequency; rarer attributes are more valuable
            rarity = 1 / frequency
            
            # The deficit is how many we still need
            deficit = max(0, needed_count)
            
            # The score contribution is the product of how much we need it (deficit) and how hard it is to find (rarity)
            score += deficit * rarity
            
        return score

    def _are_constraints_met(self):
        """
        Checks if all admission constraints have been satisfied.
        
        Returns:
            bool: True if all constraints are met, False otherwise.
        """
        for attribute, required_count in self.constraints.items():
            # If the current count for any attribute is less than what's required, we're not done
            if self.current_attribute_counts.get(attribute, 0) < required_count:
                return False
        return True

    def _get_acceptance_threshold(self):
        """
        NOTE: This method is part of a dynamic threshold strategy and is NOT USED in the current logic.
        
        Calculates a dynamic acceptance threshold based on how full the venue is.
        The idea is to be stricter at the beginning and more lenient as the venue fills up.
        
        Returns:
            float: The current threshold for accepting people.
        """
        # Calculate the current fill rate of the venue (0.0 to 1.0)
        fill_rate = self.admitted_count / VENUE_CAPACITY
        
        # Phase 1: Be very selective when the venue is mostly empty
        if self.admitted_count < self.phase1_threshold:
            threshold = self.base_threshold * (1 - fill_rate) ** 2
        # Phase 2: Moderate selectivity as we get closer to the target
        elif fill_rate < self.phase2_threshold:
            threshold = 0.3 * (1 - fill_rate) ** 2
        # Phase 3: Be very lenient to fill the last few slots
        else:
            threshold = 0.05
            
        return threshold

    def _is_feasible(self, person_attributes):
        """
        Checks if admitting this person would still allow all constraints to be met in the future.
        
        This is a critical look-ahead function to prevent getting into a state where
        the game becomes unwinnable because there aren't enough remaining slots to
        satisfy the required attribute counts.
        
        Args:
            person_attributes (dict): A dictionary mapping attribute names to boolean presence.
            
        Returns:
            bool: True if admitting the person is feasible, False otherwise.
        """
        # Calculate the number of open slots remaining in the venue after admitting this person
        remaining_slots = VENUE_CAPACITY - self.admitted_count - 1
        
        # Iterate through each constraint to check for feasibility
        for attribute, required_count in self.constraints.items():
            # Calculate how many more people with this attribute are still needed
            needed_count = required_count - self.current_attribute_counts[attribute]
            
            # If the current person has this attribute, we would need one less after admitting them
            if person_attributes.get(attribute, False):
                needed_count = max(0, needed_count - 1)
            
            # If the number of people still needed for an attribute is greater than the
            # number of remaining slots, it's impossible to meet that constraint.
            if needed_count > remaining_slots:
                return False # This decision is not feasible
                
        return True # This decision is feasible

    def _track_attribute_combinations(self, person_attributes):
        """Track attribute combinations for correlation analysis."""
        self.people_seen += 1
        
        young = person_attributes.get('young', False)
        well_dressed = person_attributes.get('well_dressed', False)
        
        if young and well_dressed:
            self.combination_counts['both_young_well_dressed'] += 1
        elif young and not well_dressed:
            self.combination_counts['young_only'] += 1
        elif not young and well_dressed:
            self.combination_counts['well_dressed_only'] += 1
        else:
            self.combination_counts['neither'] += 1

    def make_decision(self, person):
        """
        Decides whether to accept or reject a person based on the multi-phase strategy for Scenario 1.
        
        Decision Logic:
        1. Special Case: If we have 600 'young' and 600 'well_dressed', accept everyone to quickly fill the venue.
        2. Phase 1 (first 1,200 people): Accept anyone who has at least one of the required attributes.
        3. Phase 2 (after 1,200, constraints not met): 
           - If a person has attributes, accept them as long as it's feasible.
           - If a person has no attributes, only accept them if there are enough remaining slots to satisfy all constraints later.
        4. Phase 3 (constraints met): Accept everyone to fill the venue to capacity.
        """
        person_attributes = person['attributes']
        
        # Track attribute combinations for simulation improvement
        self._track_attribute_combinations(person_attributes)
        
        # Make the decision
        decision = self._make_decision_logic(person_attributes)
        
        
        return decision
    
    def _make_decision_logic(self, person_attributes):
        """Internal decision logic separated for cleaner data collection"""
        
        has_any_attribute = any(person_attributes.get(attr, False) for attr in self.constraints.keys())
        
        # Special case: If we have met the high-count constraints, accept everyone to finish quickly.
        young_count = self.current_attribute_counts.get('young', 0)
        well_dressed_count = self.current_attribute_counts.get('well_dressed', 0)
        if young_count >= 600 and well_dressed_count >= 600:
            return True
        
        # Phase 1: For the first 1,200 people, the strategy is simple.
        if self.admitted_count < self.phase1_threshold:
            # Accept if they have any required attribute, reject otherwise.
            return has_any_attribute
        
        # After Phase 1, check if all constraints have been met.
        if self._are_constraints_met():
            # Phase 3: All constraints are satisfied, so accept everyone to fill the venue.
            return True
        
        # Phase 2: Constraints are not yet met, and we are past the first 1,200 people.
        if not has_any_attribute:
            # This person has no useful attributes.
            # First, ensure admitting them doesn't make the game unwinnable.
            if not self._is_feasible(person_attributes):
                return False # Reject if it's not feasible
            
            # Calculate the total number of "attribute slots" we still need to fill.
            remaining_slots = VENUE_CAPACITY - self.admitted_count - 1
            total_needed = sum(max(0, self.constraints[attr] - self.current_attribute_counts.get(attr, 0)) 
                             for attr in self.constraints.keys())
            
            # Accept this "zero-attribute" person only if the number of remaining venue slots
            # is greater than or equal to the total number of attribute slots we still need.
            # This is a heuristic to ensure we don't waste too many slots on people who don't help.
            return remaining_slots >= total_needed
        
        # If the person has at least one attribute, accept them as long as it's feasible.
        return self._is_feasible(person_attributes)

    def _print_correlation_analysis(self):
        """Print detailed correlation analysis for simulation improvement."""
        if self.people_seen == 0:
            return
            
        print("\n--- CORRELATION ANALYSIS FOR SIMULATION IMPROVEMENT ---")
        print(f"Total people observed: {self.people_seen}")
        print("\nAttribute combination frequencies (observed in real game):")
        
        # Calculate percentages
        both_pct = (self.combination_counts['both_young_well_dressed'] / self.people_seen) * 100
        young_only_pct = (self.combination_counts['young_only'] / self.people_seen) * 100
        well_dressed_only_pct = (self.combination_counts['well_dressed_only'] / self.people_seen) * 100
        neither_pct = (self.combination_counts['neither'] / self.people_seen) * 100
        
        print(f"  Both young & well_dressed: {self.combination_counts['both_young_well_dressed']} ({both_pct:.1f}%)")
        print(f"  Young only: {self.combination_counts['young_only']} ({young_only_pct:.1f}%)")
        print(f"  Well_dressed only: {self.combination_counts['well_dressed_only']} ({well_dressed_only_pct:.1f}%)")
        print(f"  Neither: {self.combination_counts['neither']} ({neither_pct:.1f}%)")
        
        # Calculate marginal probabilities
        total_young = self.combination_counts['both_young_well_dressed'] + self.combination_counts['young_only']
        total_well_dressed = self.combination_counts['both_young_well_dressed'] + self.combination_counts['well_dressed_only']
        
        young_marginal = total_young / self.people_seen
        well_dressed_marginal = total_well_dressed / self.people_seen
        
        print(f"\nMarginal probabilities:")
        print(f"  P(young) = {young_marginal:.3f}")
        print(f"  P(well_dressed) = {well_dressed_marginal:.3f}")
        
        # Calculate correlation
        both_observed = self.combination_counts['both_young_well_dressed'] / self.people_seen
        both_independent = young_marginal * well_dressed_marginal
        
        print(f"\nCorrelation analysis:")
        print(f"  P(both | independent) = {both_independent:.3f} ({both_independent*100:.1f}%)")
        print(f"  P(both | observed) = {both_observed:.3f} ({both_observed*100:.1f}%)")
        
        if both_independent > 0:
            correlation_ratio = both_observed / both_independent
            print(f"  Correlation factor = {correlation_ratio:.2f}")
            if correlation_ratio > 1.1:
                print(f"  ✓ POSITIVE CORRELATION detected! Attributes are {correlation_ratio:.1f}x more likely to co-occur")
            elif correlation_ratio < 0.9:
                print(f"  ✗ NEGATIVE CORRELATION detected! Attributes are {1/correlation_ratio:.1f}x less likely to co-occur")
            else:
                print(f"  ~ Attributes appear roughly independent")
        
        print(f"\n--- SIMULATION FIX RECOMMENDATIONS ---")
        print(f"Update simulation_engine.py PersonGenerator to model correlated attributes:")
        print(f"  - P(both young & well_dressed) ≈ {both_observed:.3f} (not {both_independent:.3f})")
        print(f"  - Consider using a joint probability table instead of independent sampling")
        print(f"-----------------------------------------------------------")

    def run_game(self):
        """
        Runs the main game loop, from starting the game to processing each person
        until the game ends.
        """
        # Attempt to start a new game. If it fails, exit.
        if not self.start_new_game():
            return

        # Get the very first person from the queue.
        result = self._get_next_person(person_index=0)
        if not result or not result.get('nextPerson'):
            print("Failed to get the first person.")
            return

        next_person = result.get('nextPerson')

        # Main loop: continues as long as the game is 'running' and there's a next person.
        while result.get('status') == 'running' and next_person:
            # Make a decision for the current person.
            decision = self.make_decision(next_person)
            
            # Determine the current phase for logging purposes.
            if self.admitted_count < self.phase1_threshold:
                phase = 1
            elif not self._are_constraints_met():
                phase = 2
            else:
                phase = 3
                
            # Print person details and decision
            person_attrs = [attr for attr, present in next_person['attributes'].items() if present]
            fill_rate = (self.admitted_count / VENUE_CAPACITY) * 100
            if self.verbose:
                print(f"Person {next_person['personIndex']}: Attributes: {person_attrs}")
                print(f"  Phase {phase}, Venue {fill_rate:.1f}% full. Decision: {'Accept' if decision else 'Reject'}")

            # Submit the decision and get the next person.
            result = self._get_next_person(person_index=next_person['personIndex'], accept=decision)

            if not result:
                if self.verbose:
                    print("Failed to get next person. Ending game.")
                break

            # --- Update State Based on Decision ---
            if decision:
                self.admitted_count += 1
                
                # If admitted, update the counts for each attribute they possess.
                for attr, present in next_person['attributes'].items():
                    if present and attr in self.current_attribute_counts:
                        self.current_attribute_counts[attr] += 1
                
                if self.verbose:
                    print(f"  -> Admitted. Counts: {self.current_attribute_counts}")
            else:
                self.rejected_count += 1
                # Provide a reason for the rejection in the logs for better debugging.
                if self.verbose:
                    if not self._is_feasible(next_person['attributes']):
                        print(f"  -> Rejected (would make constraints impossible)")
                    else:
                        has_attr = any(next_person['attributes'].get(attr, False) for attr in self.constraints.keys())
                        if not has_attr:
                            print(f"  -> Rejected (no attributes, constraints not yet met)")
                        else:
                            print(f"  -> Rejected (other strategic reason)")

            # Move to the next person returned by the API.
            next_person = result.get('nextPerson')
            # A small delay to prevent overwhelming the server and to make the log readable.
            time.sleep(0.02)

        # --- Game End ---
        # The loop has finished, so the game is over. Print the final results.
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
                
                # Print correlation statistics for simulation improvement
                self._print_correlation_analysis()
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
                
                # Print correlation statistics for simulation improvement
                self._print_correlation_analysis()
                print("---------------------")

# This block ensures the code inside only runs when the script is executed directly
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run Berghain Challenge Scenario 1')
    parser.add_argument('--quiet', '-q', action='store_true', 
                       help='Disable verbose output (only show minimal information)')
    args = parser.parse_args()
    
    # Create an instance of our bouncer with verbose setting
    verbose = not args.quiet
    bouncer = AdaptiveBouncer(scenario=SCENARIO, player_id=PLAYER_ID, verbose=verbose)
    # Run the game
    bouncer.run_game()