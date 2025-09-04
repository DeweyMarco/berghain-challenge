# Berghain Challenge

You're the bouncer at a night club. Your goal is to fill the venue with N=1000 people while satisfying specific constraints. People arrive one by one, and you must immediately decide whether to let them in or turn them away. Your challenge is to fill the venue with as few rejections as possible while meeting all minimum requirements.

This project provides a local simulation environment and example bouncer implementations to solve this challenge.

## Getting Started

### Prerequisites
- Python 3.x

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/DeweyMarco/berghain-challenge.git
    cd berghain-challenge
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your environment:**
    -   Create a `.env` file by copying the `.env.example` file:
        ```bash
        cp .env.example .env
        ```
    -   Edit the `.env` file to add your `PLAYER_ID` and the `BASE_URL` for the game server. For local simulation, these values are used but do not need to be real.

### Running the Local Simulation

The `run_local_simulation.py` script allows you to test your bouncer logic locally without making actual API calls. It works by intercepting network requests from your bouncer script and simulating the game server's responses.

To run the simulation, use the following command:

```bash
python run_local_simulation.py <scenario_number> <path_to_bouncer_script> [--quiet]
```

-   `<scenario_number>`: The scenario to run (1, 2, or 3).
-   `<path_to_bouncer_script>`: The path to your Python script that contains your bouncer logic class.
-   `--quiet` or `-q` (optional): Disable verbose output for faster execution.

For example, to run scenario 1 with the example bouncer logic in `scenario_1/scenario_1.py`:

```bash
python run_local_simulation.py 1 scenario_1/scenario_1.py
```

The script will then instantiate your bouncer class, run the simulation, and print the results.

### Controlling Output Verbosity

Both the simulation runner and individual bouncer scripts support verbose output control:

- **Verbose mode (default)**: Shows detailed information for each person and decision
  ```bash
  python run_local_simulation.py 1 scenario_1/scenario_1.py
  # OR run individual bouncer scripts directly:
  python scenario_1/scenario_1.py
  ```

- **Quiet mode**: Shows only minimal information for faster execution
  ```bash
  python run_local_simulation.py 1 scenario_1/scenario_1.py --quiet
  # OR run individual bouncer scripts with --quiet flag:
  python scenario_1/scenario_1.py --quiet
  ```

**Verbose Output Example:**
```
Person 42: Attributes: ['young', 'well_dressed']
  Phase 1, Venue 15.2% full. Decision: Accept
  -> Admitted. Counts: {'young': 123, 'well_dressed': 98}
```

**Quiet Output**: Only shows final statistics and essential information.

## Data Collection & Distribution Analysis

The bouncer scripts automatically collect empirical data during gameplay to build more accurate population models. This addresses the limitation that while you know marginal frequencies and pairwise correlations, the exact joint distributions are unknown.

### Collecting Real Distribution Data

All bouncer scripts automatically log every person encountered to CSV files:

```bash
# Run games to collect data (automatically logged)
python scenario_1/scenario_1.py
python scenario_2/scenario_2.py  
python scenario_3/scenario_3.py
```

For systematic data collection across multiple runs:

```bash
# Collect data from 5 games for scenario 1
python data/collect_data.py 1 --runs 5

# Collect data for all scenarios
python data/collect_data.py 1 --all --runs 10 --delay 60
```

### Analyzing Collected Data

Process the collected data to build empirical distributions:

```bash
# Analyze scenario 1 (builds exact joint probability table)
python data/analyze_data.py 1

# Analyze complex scenarios (builds conditional probability models)  
python data/analyze_data.py 2 --save-results
python data/analyze_data.py 3 --save-results
```

### Generated Files

- **`scenario_X_people_data.csv`**: Raw person attributes and bouncer decisions
- **`scenario_X_runs.json`**: Game metadata, outcomes, and run statistics  
- **`scenario_X_analysis.json`**: Processed statistical analysis and distribution parameters

### Benefits

- **Scenario 1**: Exact joint probability tables for perfect 2-attribute modeling
- **Scenarios 2-3**: Conditional probability chains that preserve complex correlations
- **Validation**: Compare simulation accuracy against real API distributions
- **Iterative Improvement**: Models get better as more data is collected

The analysis scripts provide ready-to-use code for updating `simulation_engine.py` with empirically-derived distributions.

## Project Structure

-   **`run_local_simulation.py`**: The main script to run local simulations. It uses monkey-patching to intercept network calls from the bouncer scripts and redirect them to the `simulation_engine`. Enhanced with detailed probability tracking and debugging output.
-   **`simulation_engine.py`**: A local simulation of the game server. It generates a stream of "people" with attributes based on empirically-derived correlation matrices and real API frequency data. Includes progress tracking every 100 admissions and rejection count monitoring.
-   **`scenario_*/`**: Each directory contains the specific details for that scenario.
    -   **`SCENARIO*.md`**: Describes the constraints and statistical details for the scenario.
    -   **`scenario_*.py`**: An example implementation of a bouncer with a strategy tailored to that scenario. All scripts support `--quiet` flag for minimal output. **Enhanced with data collection capabilities** - automatically logs all person attributes and decisions to CSV files for distribution analysis.
-   **`collect_data.py`**: Automated data collection script that runs multiple games against real API endpoints to gather empirical distribution data.
-   **`analyze_data.py`**: Statistical analysis script that processes collected data to build accurate joint probability distributions and correlation matrices.
-   **`.env.example`**: An example environment file.
-   **`requirements.txt`**: Python dependencies.

## Common Strategic Elements

### Feasibility Checking
All strategies implement `_is_feasible()` to prevent impossible game states:
- Calculate remaining slots after accepting a person
- Ensure all constraints can still be met with remaining capacity
- Reject if any constraint becomes impossible

### Multi-Phase Logic
Different acceptance criteria based on venue fill rate and constraint satisfaction:
- Early phase: Strict criteria to "bank" valuable attributes
- Mid phase: Balanced approach with strategic flexibility
- Late phase: Lenient criteria to fill remaining slots

### Attribute Prioritization
Scoring systems based on:
- **Rarity**: Inverse of frequency (rarer = more valuable)
- **Urgency**: How many more needed vs. remaining slots
- **Combination value**: People with multiple attributes are prioritized

### Data Collection
All bouncer implementations automatically log:
- Every person encountered (attributes and decision)
- Game progression and constraint satisfaction
- Empirical distribution data for simulation improvement

## API

The simulation (and the real game) uses a simple API.

1.  **Create a new game:**
    ```
    /new-game?scenario=1&playerId=<your-player-id>
    ```
    
    Returns game data including constraints and attribute statistics:
    ```json
    {
      "gameId": "uuid",
      "constraints": [
        {"attribute": "young", "minCount": 600},
        {"attribute": "well_dressed", "minCount": 600}
      ],
      "attributeStatistics": {
        "relativeFrequencies": {
          "young": 0.322,
          "well_dressed": 0.322
        },
        "correlations": {
          "young": {"young": 1, "well_dressed": 0.183},
          "well_dressed": {"young": 0.183, "well_dressed": 1}
        }
      }
    }
    ```

2.  **Get a person and make a decision:**
    ```
    /decide-and-next?gameId=uuid&personIndex=0&accept=true
    ```

**Data Collection**: All bouncer scripts automatically log API interactions to CSV files for empirical distribution analysis, enabling more accurate local simulations.

## Implementation Details

### Simulation Engine Features

The `simulation_engine.py` provides a sophisticated local simulation environment:

- **Empirical Data Integration**: Uses real API frequency data and correlation matrices from collected data
- **Scenario Detection**: Automatically detects scenarios based on constraint attributes (young+well_dressed = Scenario 1, techno_lover+well_connected+creative+berlin_local = Scenario 2, etc.)
- **Correlation Modeling**: 
  - Scenario 1: Joint probability tables for exact 2-attribute modeling using observed frequencies
  - Scenarios 2-3: Independent generation with correlation matrices for complex attribute relationships
- **Progress Tracking**: Monitors admission counts every 100 people and provides detailed progress updates
- **Feasibility Checking**: Prevents impossible game states by tracking remaining capacity vs. constraint requirements

### Bouncer Strategy Implementation

The example bouncer implementations demonstrate key strategic concepts:

- **Scenario 1**: Multi-phase logic with 1200-person threshold, feasibility checking, and strategic attribute management
- **Scenario 2**: Creative-first strategy with concurrent constraint optimization and phase-based attribute building
- **Scenario 3**: Critical bottleneck management with german speaker constraint tracking and advanced scoring
- **Common Features**: All implement feasibility checking, multi-phase logic, and automatic data collection

### Data Analysis Pipeline

The data collection and analysis tools provide:

- **Automated Collection**: Systematic data gathering across multiple game runs using simple "reject 19, select 1" algorithm
- **Statistical Analysis**: 
  - Scenario 1: Joint probability tables and exact correlation analysis
  - Scenarios 2-3: Marginal probabilities and pairwise correlations
- **Simulation Integration**: Ready-to-use code snippets for updating the simulation engine with empirical data
- **Quality Assurance**: Validation against real API distributions with correlation factor analysis

### Key Implementation Methods

**Feasibility Checking** (`_is_feasible`):
```python
def _is_feasible(self, person_attributes):
    remaining_slots = VENUE_CAPACITY - self.admitted_count - 1
    for attribute, required_count in self.constraints.items():
        needed_count = required_count - self.current_attribute_counts[attribute]
        if person_attributes.get(attribute, False):
            needed_count = max(0, needed_count - 1)
        if needed_count > remaining_slots:
            return False
    return True
```

**Multi-Phase Decision Logic**:
- Phase transitions based on venue fill rate and constraint satisfaction
- Different acceptance criteria for each phase
- Strategic flexibility as game progresses

**Data Collection**:
- Automatic logging of every person encountered
- Attribute combination tracking for correlation analysis
- Game progression and constraint satisfaction monitoring

## Advanced Usage

### Custom Bouncer Development

To create your own bouncer strategy:

1. **Study the existing implementations**: Each scenario has a different strategic approach
   - `scenario_1/scenario_1.py`: Multi-phase constraint management
   - `scenario_2/scenario_2.py`: Creative-first concurrent optimization  
   - `scenario_3/scenario_3.py`: Critical bottleneck management

2. **Implement required methods**:
   - `start_new_game()`: Initialize game state and constraints
   - `make_decision(person)`: Core decision logic
   - `run_game()`: Main game loop

3. **Key strategic considerations**:
   - Always implement `_is_feasible()` to prevent impossible states
   - Use multi-phase logic based on venue fill rate
   - Prioritize rare attributes that are constraint bottlenecks
   - Collect data for empirical distribution analysis

4. **Test locally**: Use `run_local_simulation.py` to test without API calls

### Simulation Engine Customization

The simulation engine can be extended with:

- **Custom attribute generation**: Modify `PersonGenerator.generate_person()` for different distributions
- **Additional correlation models**: Add new scenario configurations with custom correlation matrices
- **Performance metrics**: Extend `SimulationEngine` with additional tracking and analysis
- **External data integration**: Import empirical distributions from data analysis results

### Data-Driven Strategy Optimization

Use the collected data to:

- **Validate strategy assumptions**: Compare expected vs. observed attribute frequencies
- **Optimize thresholds**: Analyze phase transition points for optimal performance
- **Identify bottlenecks**: Find which attributes are most constraining
- **Improve simulation accuracy**: Update `simulation_engine.py` with empirical distributions

### Example: Updating Simulation Engine

After running data analysis, you can update the simulation engine:

```python
# In simulation_engine.py, update the joint probabilities:
self.joint_probabilities = {
    (False, False): 0.5024,  # From empirical data
    (False, True): 0.1827,   
    (True, False): 0.1753,   
    (True, True): 0.1396     
}
```

This ensures your local simulation matches real API behavior exactly.

