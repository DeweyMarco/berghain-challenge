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
SCENARIO = 3 # Scenario to run (1, 2, or 3)

RETRY_ATTEMPTS = 3
RETRY_DELAY = 1  # in seconds
VENUE_CAPACITY = 1000


class AdaptiveBouncer:
    """
    An adaptive bouncer that balances constraint satisfaction with venue filling.
    
    The algorithm works by:
    1. Being very selective early to ensure constraints can be met
    2. Gradually becoming more lenient as the venue fills up
    3. Using constraint satisfaction scoring to prioritize valuable people
    4. Always checking feasibility before accepting anyone
    """
    
    def __init__(self, scenario, player_id, verbose=True):
        """
        Initialize the adaptive bouncer with game parameters.
        
        Args:
            scenario: Which game scenario to play (1, 2, or 3)
            player_id: Unique identifier for tracking progress
            verbose (bool): Whether to enable verbose printing.
        """
        self.scenario = scenario
        self.player_id = player_id
        self.verbose = verbose
        self.game_id = None  # Will be set when we start a new game
        
        # Game constraints and tracking
        self.constraints = {}  # {"attribute": minCount}
        self.attribute_stats = {}  # Population statistics for rarity calculation
        self.current_attribute_counts = {}  # Current counts of each attribute
        
        # Game state tracking
        self.admitted_count = 0
        self.rejected_count = 0
        
        
        # Algorithm parameters
        self.base_threshold = 0.7  # Base threshold for early phase
        self.phase1_threshold = 0.6  # End of strict phase (60% full)
        self.phase2_threshold = 0.9  # End of balanced phase (90% full)

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

    def _should_accept_advanced(self, person_attributes):
        """
        Advanced decision logic using urgency-based scoring and multi-constraint bonuses.
        
        Calculates score based on:
        1. Urgency (how desperately we need each attribute)
        2. Rarity weighting (rarer attributes get higher priority)
        3. Multi-constraint bonus (people helping multiple constraints)
        
        Args:
            person_attributes: Dict mapping attribute names to boolean presence
            
        Returns:
            True if person should be accepted, False otherwise
        """
        score = 0
        helpful_constraints = 0
        debug_info = []
        
        for attr, present in person_attributes.items():
            if not present or attr not in self.constraints:
                continue
                
            needed = self.constraints[attr] - self.current_attribute_counts.get(attr, 0)
            if needed <= 0:
                continue
                
            helpful_constraints += 1
            frequency = self.attribute_stats['relativeFrequencies'].get(attr, 0.001)
            
            # Calculate urgency: how desperate we are for this attribute
            remaining_capacity = VENUE_CAPACITY - self.admitted_count
            urgency = needed / remaining_capacity if remaining_capacity > 0 else float('inf')
            
            # Rarity weight: rarer attributes get exponentially higher priority
            rarity_weight = 1 / frequency
            
            # Score contribution: urgency × rarity
            contribution = urgency * rarity_weight
            score += contribution
            
            debug_info.append(f"{attr}: urgency={urgency:.2f}, rarity={rarity_weight:.1f}, contrib={contribution:.2f}")
        
        # Multi-constraint bonus: people who help with multiple constraints are valuable
        if helpful_constraints >= 2:
            score *= 1.5
        if helpful_constraints >= 3:
            score *= 2.0
            
        # Get dynamic threshold based on desperation
        threshold = self._get_desperation_threshold()
        
        # Debug output for people with significant scores
        if score > threshold * 0.5 and self.verbose:
            multi_bonus = f" (×{1.5 if helpful_constraints >= 2 else 2.0 if helpful_constraints >= 3 else 1.0} multi-bonus)" if helpful_constraints >= 2 else ""
            print(f"    Advanced score: {score:.3f} vs threshold {threshold:.3f}{multi_bonus}")
            if debug_info:
                print(f"    Breakdown: {' + '.join(debug_info)}")
            
        return score >= threshold

    def _are_constraints_met(self):
        """
        Checks if all constraints have been satisfied.
        
        Returns:
            True if all constraints are met, False otherwise
        """
        for attribute, required_count in self.constraints.items():
            if self.current_attribute_counts.get(attribute, 0) < required_count:
                return False
        return True

    def _get_desperation_threshold(self):
        """
        Calculates dynamic threshold based on constraint urgency.
        
        The more desperate we are to meet constraints, the lower the threshold.
        This ensures we become more lenient when constraints are at risk.
        
        Returns:
            Current threshold value for accepting people
        """
        max_desperation = 0
        remaining_slots = VENUE_CAPACITY - self.admitted_count
        
        if remaining_slots <= 0:
            return 0  # Accept everyone if no slots left (shouldn't happen)
        
        # Calculate desperation for each constraint
        for attr, required in self.constraints.items():
            current = self.current_attribute_counts.get(attr, 0)
            needed = required - current
            
            if needed > 0:
                # Desperation = what fraction of remaining slots we need for this constraint
                desperation = needed / remaining_slots
                max_desperation = max(max_desperation, desperation)
        
        # Base threshold starts high, but decreases as desperation increases
        base_threshold = 2.0  # Start with high standards
        
        # Lower threshold when more desperate (exponential decay)
        dynamic_threshold = base_threshold * (1 - max_desperation) ** 2
        
        # Never go below minimum threshold
        return max(0.1, dynamic_threshold)

    def _is_feasible(self, person_attributes):
        """
        Checks if accepting this person would still allow us to meet all constraints.
        
        This is a critical check to ensure we don't accept someone who would
        make it impossible to satisfy the remaining constraints.
        
        Args:
            person_attributes: Dict mapping attribute names to boolean presence
            
        Returns:
            True if accepting maintains feasibility, False otherwise
        """
        # Calculate remaining slots after accepting this person
        remaining_slots = VENUE_CAPACITY - self.admitted_count - 1
        
        # Check each constraint to see if we can still meet it
        for attribute, required_count in self.constraints.items():
            # Calculate how many more people with this attribute we need
            needed_count = required_count - self.current_attribute_counts[attribute]
            
            # If this person has this attribute, we need one less
            if person_attributes.get(attribute, False):
                needed_count = max(0, needed_count - 1)
            
            # If we need more people with this attribute than we have slots left,
            # accepting this person would make it impossible to meet the constraint
            if needed_count > remaining_slots:
                if self.verbose:
                    print(f"    Feasibility check FAILED: {attribute} needs {needed_count} more but only {remaining_slots} slots remain")
                return False
                
        return True

    def make_decision(self, person):
        """
        Decides whether to accept or reject using mathematically optimized logic.
        
        Decision logic (in priority order):
        1. Feasibility check: reject if accepting would make constraints impossible
        2. If all constraints met: accept everyone to fill the venue  
        3. ALWAYS accept critical bottlenecks (queer_friendly, vinyl_collector)
        4. German speaker constraint management (max 200 non-german speakers)
        5. Advanced scoring for remaining decisions
        
        Args:
            person: Person object with attributes and metadata
            
        Returns:
            True to accept, False to reject
        """
        person_attributes = person['attributes']
        
        # Make the decision
        decision = self._make_decision_logic(person_attributes)
        
        
        return decision
    
    def _make_decision_logic(self, person_attributes):
        """Internal decision logic separated for cleaner data collection"""
        
        # Phase 1: Feasibility check - never make constraints impossible
        if not self._is_feasible(person_attributes):
            return False

        # Phase 2: If all constraints met, fill remaining slots
        if self._are_constraints_met():
            return True

        # Phase 3: ALWAYS accept the critical bottlenecks (rarest attributes)
        if (person_attributes.get('queer_friendly', False) or 
            person_attributes.get('vinyl_collector', False)):
            return True
        
        # Phase 4: German speaker constraint management
        german_speaker = person_attributes.get('german_speaker', False)
        max_non_german = VENUE_CAPACITY - self.constraints.get('german_speaker', 0)  # 1000 - 800 = 200
        current_non_german = self.admitted_count - self.current_attribute_counts.get('german_speaker', 0)
        remaining_non_german_slots = max_non_german - current_non_german
        
        # Reject non-german speakers if we've hit our limit (need 80% german speakers)
        if not german_speaker and remaining_non_german_slots <= 0:
            return False
        
        # Phase 5: Advanced scoring for remaining decisions
        return self._should_accept_advanced(person_attributes)

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
            if self.verbose:
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

            # Update our tracking variables based on our decision
            if decision:
                # We accepted this person
                self.admitted_count += 1
                
                # Update counts for each attribute this person has
                for attr, present in next_person['attributes'].items():
                    if present and attr in self.current_attribute_counts:
                        self.current_attribute_counts[attr] += 1
                
                if self.verbose:
                    print(f"  -> Admitted. Counts: {self.current_attribute_counts}")
            else:
                # We rejected this person
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
    parser = argparse.ArgumentParser(description='Run Berghain Challenge Scenario 3')
    parser.add_argument('--quiet', '-q', action='store_true', 
                       help='Disable verbose output (only show minimal information)')
    args = parser.parse_args()
    
    # Create an instance of our bouncer with verbose setting
    verbose = not args.quiet
    bouncer = AdaptiveBouncer(scenario=SCENARIO, player_id=PLAYER_ID, verbose=verbose)
    bouncer.run_game()
