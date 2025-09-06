
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
            # Joint probabilities from observed behavior for scenario 2
            self.joint_probabilities = {
                (False, False, True, True): 0.09824164878945756,    # P(berlin_local=False, creative=False, techno_lover=True, well_connected=True)
                (False, False, True, False): 0.4177329144958627,    # P(berlin_local=False, creative=False, techno_lover=True, well_connected=False)
                (True, False, False, True): 0.24651394422310757,    # P(berlin_local=True, creative=False, techno_lover=False, well_connected=True)
                (True, False, True, False): 0.013790989886607416,   # P(berlin_local=True, creative=False, techno_lover=True, well_connected=False)
                (True, True, True, True): 0.025896414342629483,     # P(berlin_local=True, creative=True, techno_lover=True, well_connected=True)
                (True, False, False, False): 0.04863239350291143,  # P(berlin_local=True, creative=False, techno_lover=False, well_connected=False)
                (True, False, True, True): 0.04752145265093472,    # P(berlin_local=True, creative=False, techno_lover=True, well_connected=True)
                (False, False, False, True): 0.03162350597609562,  # P(berlin_local=False, creative=False, techno_lover=False, well_connected=True)
                (False, False, False, False): 0.03505209929512718, # P(berlin_local=False, creative=False, techno_lover=False, well_connected=False)
                (True, True, True, False): 0.007738277658596384,   # P(berlin_local=True, creative=True, techno_lover=True, well_connected=False)
                (True, True, False, True): 0.006838032485442844,   # P(berlin_local=True, creative=True, techno_lover=False, well_connected=True)
                (False, True, True, True): 0.010247471651854122,   # P(berlin_local=False, creative=True, techno_lover=True, well_connected=True)
                (False, True, False, True): 0.0028539687404229236, # P(berlin_local=False, creative=True, techno_lover=False, well_connected=True)
                (False, True, True, False): 0.0049800796812749,    # P(berlin_local=False, creative=True, techno_lover=True, well_connected=False)
                (True, True, False, False): 0.0015897946674839104, # P(berlin_local=True, creative=True, techno_lover=False, well_connected=False)
                (False, True, False, False): 0.000747011952191235  # P(berlin_local=False, creative=True, techno_lover=False, well_connected=False)
            }
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
            # Joint probabilities from observed behavior for scenario 3
            self.joint_probabilities = {
                (True, False, True, False, True, False): 0.2606859024844276,   # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (False, True, False, False, True, False): 0.1567981671081836,  # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (True, False, True, False, False, False): 0.15173265554521373, # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (True, True, False, False, True, False): 0.10150712393498962,  # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (True, True, False, False, False, False): 0.06502828094794874, # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (False, False, True, False, True, False): 0.0439428653254099,  # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (True, True, True, False, True, False): 0.02534545714899406,   # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (False, True, False, False, False, False): 0.021998281663922103, # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (True, True, True, False, False, False): 0.019886160234839263, # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (False, False, True, False, False, False): 0.016252595403450993, # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (False, True, True, False, True, False): 0.013800386625617528,  # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (True, False, False, False, True, False): 0.013191809264695353, # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (False, False, False, False, False, False): 0.013156010596405813, # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (True, False, False, False, False, False): 0.01267272857449703, # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (False, True, False, False, True, True): 0.007213431660342235,  # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (False, False, False, False, True, False): 0.006873344311591608, # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=False)
                (False, True, True, False, False, False): 0.00678384764086776,  # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=False)
                (True, False, True, True, True, False): 0.004958115558101239,   # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (True, True, True, True, True, True): 0.004206343524020906,     # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (False, True, True, False, True, True): 0.0039199541777045896,  # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (True, True, True, True, True, False): 0.0033650748192167253,  # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (False, True, False, True, True, True): 0.0029712894680317893,  # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (True, True, False, True, True, False): 0.00289969213145271,   # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (True, False, True, True, True, True): 0.0028638934631631703,  # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (True, True, False, True, True, True): 0.0025596047827020833,  # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (False, True, True, True, True, True): 0.002398510775399155,   # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (True, False, True, True, False, False): 0.0020763227607932984, # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (True, True, False, False, True, True): 0.002022624758358989,   # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (True, False, False, True, True, False): 0.00191522875349037,  # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (False, True, False, True, True, False): 0.0018615307510560608, # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (False, False, False, False, True, True): 0.0015930407388845135, # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (True, False, False, True, True, True): 0.0015751414047397436,  # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (True, True, True, False, True, True): 0.0014856447340158947,   # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (True, True, True, True, False, False): 0.0015214434023054343,  # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (False, False, True, False, True, True): 0.0013424500608577362,  # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (True, True, False, True, False, False): 0.0012350540559891172, # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (True, False, True, False, True, True): 0.001252953390133887,   # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (False, True, True, True, True, False): 0.0011276580511204984,  # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (False, False, True, True, True, False): 0.0010739600486861889, # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (True, True, True, True, False, True): 0.0010202620462518794,   # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (False, False, False, True, True, True): 0.0009486647096728001, # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (False, False, True, True, True, True): 0.0009307653755280304,  # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=True, vinyl_collector=True)
                (True, False, False, True, False, False): 0.000859168038948951,  # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (True, False, True, True, False, True): 0.0008233693706594115,  # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (False, True, False, False, False, True): 0.0008054700365146416, # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
                (False, True, True, False, False, True): 0.0007159733657907926,  # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
                (True, False, False, True, False, True): 0.0006980740316460227,  # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (True, True, False, True, False, True): 0.0006801746975012529,  # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (False, False, False, True, True, False): 0.0006622753633564832, # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=True, vinyl_collector=False)
                (True, False, True, False, False, True): 0.0006443760292117133,  # P(fashion_forward=True, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
                (True, False, False, False, True, True): 0.0005190806901983246,  # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=True, vinyl_collector=True)
                (False, False, True, True, False, True): 0.00041168468532970574,  # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (False, True, False, True, False, True): 0.0003758860170401661,  # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (False, True, True, True, False, False): 0.0003579866828953963,  # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (False, False, True, True, False, False): 0.0003579866828953963,  # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (False, True, False, True, False, False): 0.0003579866828953963,  # P(fashion_forward=False, german_speaker=True, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (False, True, True, True, False, True): 0.0003579866828953963,   # P(fashion_forward=False, german_speaker=True, international=True, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (False, False, False, True, False, True): 0.00032218801460585667,  # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=True)
                (False, False, False, True, False, False): 0.0002684900121715472, # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=True, underground_veteran=False, vinyl_collector=False)
                (True, True, False, False, False, True): 0.0002684900121715472,  # P(fashion_forward=True, german_speaker=True, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
                (True, True, True, False, False, True): 0.00017899334144769814,   # P(fashion_forward=True, german_speaker=True, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
                (False, False, True, False, False, True): 0.00016109400730292834, # P(fashion_forward=False, german_speaker=False, international=True, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
                (False, False, False, False, False, True): 0.0001252953390133887, # P(fashion_forward=False, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
                (True, False, False, False, False, True): 5.369800243430944e-05  # P(fashion_forward=True, german_speaker=False, international=False, queer_friendly=False, underground_veteran=False, vinyl_collector=True)
            }
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
        
        # Use joint probabilities to maintain observed correlations for all scenarios
        if hasattr(self, 'joint_probabilities') and self.joint_probabilities is not None:
            # Generate correlated attributes using joint probabilities
            rand_val = random.random()
            cumulative = 0.0
            
            # Determine attribute order based on scenario
            scenario_1_attrs = {'young', 'well_dressed'}
            scenario_2_attrs = {'techno_lover', 'well_connected', 'creative', 'berlin_local'}
            scenario_3_attrs = {'underground_veteran', 'international', 'fashion_forward', 
                               'queer_friendly', 'vinyl_collector', 'german_speaker'}
            
            constraint_attrs = set(self.constraints.keys())
            
            if constraint_attrs == scenario_1_attrs:
                # Scenario 1: (young, well_dressed)
                for (young_val, well_dressed_val), prob in self.joint_probabilities.items():
                    cumulative += prob
                    if rand_val <= cumulative:
                        attributes['young'] = young_val
                        attributes['well_dressed'] = well_dressed_val
                        break
            elif constraint_attrs == scenario_2_attrs:
                # Scenario 2: (berlin_local, creative, techno_lover, well_connected)
                for (berlin_local_val, creative_val, techno_lover_val, well_connected_val), prob in self.joint_probabilities.items():
                    cumulative += prob
                    if rand_val <= cumulative:
                        attributes['berlin_local'] = berlin_local_val
                        attributes['creative'] = creative_val
                        attributes['techno_lover'] = techno_lover_val
                        attributes['well_connected'] = well_connected_val
                        break
            elif constraint_attrs == scenario_3_attrs:
                # Scenario 3: (fashion_forward, german_speaker, international, queer_friendly, underground_veteran, vinyl_collector)
                for (fashion_forward_val, german_speaker_val, international_val, queer_friendly_val, underground_veteran_val, vinyl_collector_val), prob in self.joint_probabilities.items():
                    cumulative += prob
                    if rand_val <= cumulative:
                        attributes['fashion_forward'] = fashion_forward_val
                        attributes['german_speaker'] = german_speaker_val
                        attributes['international'] = international_val
                        attributes['queer_friendly'] = queer_friendly_val
                        attributes['underground_veteran'] = underground_veteran_val
                        attributes['vinyl_collector'] = vinyl_collector_val
                        break
        else:
            # Fallback to independent generation if joint probabilities not available
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
