
import random
import json

class PersonGenerator:
    """Generates people based on predefined attribute probabilities for different scenarios."""
    def __init__(self, scenario_config, scenario_number=None):
        self.scenario_config = scenario_config
        self.constraints = scenario_config['constraints']
        
        # Define expected attribute sets for each scenario
        scenario_1_attrs = {'young', 'well_dressed'}
        scenario_2_attrs = {'techno_lover', 'well_connected', 'creative', 'berlin_local'}
        scenario_3_attrs = {'underground_veteran', 'international', 'fashion_forward', 
                           'queer_friendly', 'vinyl_collector', 'german_speaker'}
        
        constraint_attrs = set(self.constraints.keys())
        
        # Determine scenario based on explicit number or constraint matching
        if scenario_number:
            detected_scenario = scenario_number
        elif constraint_attrs == scenario_1_attrs:
            detected_scenario = 1
        elif constraint_attrs == scenario_2_attrs:
            detected_scenario = 2
        elif constraint_attrs == scenario_3_attrs:
            detected_scenario = 3
        else:
            raise ValueError(f"Unable to determine scenario. Constraints: {constraint_attrs}")
        
        # Scenario-specific attribute frequencies and joint probabilities
        if detected_scenario == 1:
            # Use observed marginal probabilities from scenario data
            self.attribute_frequencies = {
                'young': 0.3149,
                'well_dressed': 0.3223
            }
            # Joint probabilities from observed behavior
            self.joint_probabilities = {
                (False, False): 0.5024,  # P(young=False, well_dressed=False)
                (False, True): 0.1827,   # P(young=False, well_dressed=True)
                (True, False): 0.1753,   # P(young=True, well_dressed=False)
                (True, True): 0.1396     # P(young=True, well_dressed=True)
            }
            # Scenario 1 correlations: young and well_dressed correlation
            self.correlations = {
                'young': {
                    'young': 1,
                    'well_dressed': 0.1756  # Observed correlation
                },
                'well_dressed': {
                    'young': 0.1756,  # Observed correlation
                    'well_dressed': 1
                }
            }
        elif detected_scenario == 2:
            self.attribute_frequencies = {
                'techno_lover': 0.6265000000000001,
                'well_connected': 0.4700000000000001,
                'creative': 0.06227,
                'berlin_local': 0.398
            }
            self.joint_probabilities = None  # Use independent generation for scenario 2
            # Scenario 2 correlations
            self.correlations = {
                'techno_lover': {
                    'techno_lover': 1,
                    'well_connected': -0.4696169332674324,
                    'creative': 0.09463317039891586,
                    'berlin_local': -0.6549403815606182
                },
                'well_connected': {
                    'techno_lover': -0.4696169332674324,
                    'well_connected': 1,
                    'creative': 0.14197259140471485,
                    'berlin_local': 0.5724067808436452
                },
                'creative': {
                    'techno_lover': 0.09463317039891586,
                    'well_connected': 0.14197259140471485,
                    'creative': 1,
                    'berlin_local': 0.14446459505650772
                },
                'berlin_local': {
                    'techno_lover': -0.6549403815606182,
                    'well_connected': 0.5724067808436452,
                    'creative': 0.14446459505650772,
                    'berlin_local': 1
                }
            }
        elif detected_scenario == 3:
            self.attribute_frequencies = {
                'underground_veteran': 0.6794999999999999,
                'international': 0.5735,
                'fashion_forward': 0.6910000000000002,
                'queer_friendly': 0.04614,
                'vinyl_collector': 0.044539999999999996,
                'german_speaker': 0.4565000000000001
            }
            self.joint_probabilities = None  # Use independent generation for scenario 3
            # Scenario 3 correlations
            self.correlations = {
                'underground_veteran': {
                    'underground_veteran': 1,
                    'international': -0.08110175777152992,
                    'fashion_forward': -0.1696563475505309,
                    'queer_friendly': 0.03719928376753885,
                    'vinyl_collector': 0.07223521156389842,
                    'german_speaker': 0.11188766703422799
                },
                'international': {
                    'underground_veteran': -0.08110175777152992,
                    'international': 1,
                    'fashion_forward': 0.375711059360155,
                    'queer_friendly': 0.0036693314388711686,
                    'vinyl_collector': -0.03083247098181075,
                    'german_speaker': -0.7172529382519395
                },
                'fashion_forward': {
                    'underground_veteran': -0.1696563475505309,
                    'international': 0.375711059360155,
                    'fashion_forward': 1,
                    'queer_friendly': -0.0034530926793377476,
                    'vinyl_collector': -0.11024719606358546,
                    'german_speaker': -0.3521024461597403
                },
                'queer_friendly': {
                    'underground_veteran': 0.03719928376753885,
                    'international': 0.0036693314388711686,
                    'fashion_forward': -0.0034530926793377476,
                    'queer_friendly': 1,
                    'vinyl_collector': 0.47990640803167306,
                    'german_speaker': 0.04797381132680503
                },
                'vinyl_collector': {
                    'underground_veteran': 0.07223521156389842,
                    'international': -0.03083247098181075,
                    'fashion_forward': -0.11024719606358546,
                    'queer_friendly': 0.47990640803167306,
                    'vinyl_collector': 1,
                    'german_speaker': 0.09984452286269897
                },
                'german_speaker': {
                    'underground_veteran': 0.11188766703422799,
                    'international': -0.7172529382519395,
                    'fashion_forward': -0.3521024461597403,
                    'queer_friendly': 0.04797381132680503,
                    'vinyl_collector': 0.09984452286269897,
                    'german_speaker': 1
                }
            }
        else:
            raise ValueError(f"Invalid scenario number: {detected_scenario}")

    def generate_person(self):
        """Generates a single person with attributes based on observed probabilities."""
        # Initialize all constraint attributes as False
        attributes = {attr: False for attr in self.constraints}
        
        # For scenario 1, use joint probabilities to maintain observed correlations
        if hasattr(self, 'joint_probabilities') and self.joint_probabilities is not None:
            # Generate correlated attributes using joint probabilities
            rand_val = random.random()
            cumulative = 0.0
            
            for (young_val, well_dressed_val), prob in self.joint_probabilities.items():
                cumulative += prob
                if rand_val <= cumulative:
                    attributes['young'] = young_val
                    attributes['well_dressed'] = well_dressed_val
                    break
        else:
            # For other scenarios, use independent generation
            attributes.update({
                attr: random.random() <= freq 
                for attr, freq in self.attribute_frequencies.items()
            })
        
        return {'attributes': attributes}

class SimulationEngine:
    """Simulates the Berghain Challenge game locally for a given scenario configuration."""
    def __init__(self, scenario_config, scenario_number=None):
        self.config = scenario_config
        self.person_generator = PersonGenerator(scenario_config, scenario_number)
        self.game_id = "local-sim-game"
        self.person_index = 0
        self.admitted_count = 0
        self.rejected_count = 0
        self.current_attribute_counts = {attr: 0 for attr in self.config['constraints']}
        self.status = "not_started"
        self.max_rejections = 20000
        self.venue_capacity = self.config['venue_capacity']
        self.last_person_sent = None

    def start_game(self):
        """Initializes and starts a new game simulation, returning the initial game state."""
        self.person_index = 0
        self.admitted_count = 0
        self.rejected_count = 0
        self.current_attribute_counts = {attr: 0 for attr in self.config['constraints']}
        self.status = "running"
        self.last_person_sent = None
        
        print("--- LOCAL SIMULATION STARTED ---")
        print(f"Scenario constraints: {self.config['constraints']}")
        print(f"Venue capacity: {self.venue_capacity}")
        print(f"Attribute frequencies: {self.person_generator.attribute_frequencies}")
        
        game_data = {
            "gameId": self.game_id,
            "constraints": [{"attribute": k, "minCount": v} for k, v in self.config['constraints'].items()],
            "attributeStatistics": {
                "relativeFrequencies": self.person_generator.attribute_frequencies,
                "correlations": self.person_generator.correlations
            }
        }
        return game_data

    def decide_and_next(self, decision=None):
        """Processes a decision for the previous person and returns the next person or game status."""
        if self.status != "running":
            return {"status": self.status, "reason": "Game is not running."}

        # Process the decision for the *previous* person, if a decision was made.
        # The first call for person 0 has no preceding decision.
        if decision is not None and self.last_person_sent is not None:
            person_attrs = [attr for attr, present in self.last_person_sent['attributes'].items() if present]
            if decision:
                self.admitted_count += 1
                print(f"ADMITTED person {self.last_person_sent['personIndex']} with attributes: {person_attrs}")
                # Update counts based on the attributes of the person just processed
                for attr, present in self.last_person_sent['attributes'].items():
                    if present and attr in self.current_attribute_counts:
                        self.current_attribute_counts[attr] += 1
                
                # Print progress every 100 admissions
                if self.admitted_count % 100 == 0:
                    print(f"Progress update - Admitted: {self.admitted_count}, Rejected: {self.rejected_count}")
                    print(f"Current attribute counts: {self.current_attribute_counts}")
                    print(f"Required constraints: {self.config['constraints']}")
            else:
                self.rejected_count += 1
                if self.rejected_count % 1000 == 0:
                    print(f"Rejected {self.rejected_count} people so far...")

        # Check for game over conditions
        if self.admitted_count >= self.venue_capacity:
            self.status = "completed"
            print("--- LOCAL SIMULATION COMPLETED: Venue full ---")
            return self._get_final_state()
            
        if self.rejected_count >= self.max_rejections:
            self.status = "failed"
            print("--- LOCAL SIMULATION FAILED: Too many rejections ---")
            return self._get_final_state()

        # Generate the next person for the bouncer to evaluate
        next_person = self.person_generator.generate_person()
        next_person['personIndex'] = self.person_index
        self.last_person_sent = next_person  # Store for the next decision cycle
        self.person_index += 1

        return {
            "status": self.status,
            "nextPerson": next_person,
            "rejectedCount": self.rejected_count,
        }
        
    def _get_final_state(self):
        """Constructs the final game state response."""
        return {
            "status": self.status,
            "rejectedCount": self.rejected_count,
            "admittedCount": self.admitted_count,
            "attributeCounts": self.current_attribute_counts,
            "reason": f"Game ended with status: {self.status}"
        }
