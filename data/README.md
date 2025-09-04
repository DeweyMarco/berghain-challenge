# Data Collection and Analysis Tools

This folder contains tools for collecting and analyzing data from the Berghain Challenge simulation to build empirical probability models.

## Files Overview

- **`collect_data.py`** - Data collection script that runs multiple games to gather distribution data
- **`analyze_data.py`** - Analysis script that processes collected data to build probability models and predict person type distributions
- **`scenario_1_people_data.csv`** - Collected data from Scenario 1 games (young, well_dressed)
- **`scenario_2_people_data.csv`** - Collected data from Scenario 2 games (berlin_local, creative, techno_lover, well_connected)
- **`scenario_3_people_data.csv`** - Collected data from Scenario 3 games (fashion_forward, german_speaker, international, queer_friendly, underground_veteran, vinyl_collector)
- **`scenario_X_runs.json`** - Summary statistics from scenario runs (when generated)

## Quick Start

### 1. Collect Data

To collect data for a specific scenario:

```bash
# Collect data for Scenario 1 (5 runs with 30s delays)
python data/collect_data.py 1

# Collect data for Scenario 2 with custom settings
python data/collect_data.py 2 --runs 10 --delay 60

# Collect data for all scenarios
python data/collect_data.py 1 --all
```

**Command Line Options:**
- `scenario`: Scenario number (1, 2, or 3)
- `--runs`: Number of games to run (default: 5)
- `--delay`: Seconds between runs (default: 30)
- `--all`: Run all scenarios sequentially

### 2. Analyze Data

To analyze collected data and generate probability models:

```bash
# Basic analysis - shows correlations and probabilities
python data/analyze_data.py 1

# Full analysis with person type predictions
python data/analyze_data.py 1 --predict-types

# Analyze with predictions and save results
python data/analyze_data.py 2 --predict-types --save-results

# Analyze all aspects of scenario 3
python data/analyze_data.py 3 --predict-types --save-results
```

**Command Line Options:**
- `scenario`: Scenario number (1, 2, or 3)
- `--predict-types`: Analyze person type distributions and generate prediction code
- `--save-results`: Save analysis results to JSON file

## Data Collection Strategy

The data collection uses a simple "reject 19, select 1" algorithm to maximize the number of people seen:

- **Algorithm**: Reject 19 consecutive people, then accept 1 (20-person cycle)
- **Purpose**: Maximize data collection while maintaining game viability
- **Output**: CSV with individual person data and JSON with run summaries

## Data Structure

### People Data CSV (`scenario_X_people_data.csv`)
Each row represents one person seen during a game:
- `run_id`: Unique identifier for the data collection run
- `game_id`: Game identifier from the API
- `person_index`: Person's position in the queue
- `decision`: Whether the person was admitted (True) or rejected (False)
- Attribute columns: Boolean values for each person attribute

### Run Summary JSON (`scenario_X_runs.json`)
Summary statistics for each completed game:
- `run_id`: Unique run identifier
- `game_id`: Game identifier
- `timestamp`: When the run completed
- `scenario`: Scenario number
- `final_stats`: Game completion statistics

## Analysis Output

### Basic Analysis (All Scenarios)
- **Marginal probabilities**: Frequency of each attribute (e.g., P(young=True))
- **Pairwise correlations**: How attributes relate to each other
- **Conditional probabilities**: P(attr_A=True | attr_B=value) for scenarios 2 & 3
- **Simulation engine updates**: Ready-to-use frequency and correlation values

### Person Type Prediction (--predict-types flag)
When using `--predict-types`, the analysis additionally provides:

- **Person type distribution**: Complete frequency breakdown of all unique person combinations found in data
- **Empirical modeling**: Exact probabilities for each person type (e.g., "young + well_dressed" = 14.01%)
- **Sample generation**: 10 example persons generated using the learned distribution
- **Simulation code**: Ready-to-use `generate_person()` method that samples from empirical distribution instead of independent probabilities

#### Example Person Types Output:
```
Scenario 1 - Found 4 unique person types:
(¬well_dressed, ¬young)     | Count: 12051 | Prob: 0.5010
(well_dressed)              | Count:  4395 | Prob: 0.1827  
(young)                     | Count:  4238 | Prob: 0.1762
(well_dressed, young)       | Count:  3369 | Prob: 0.1401

Scenario 2 - Found 16 unique person types:
(techno_lover)              | Count:  4753 | Prob: 0.4128
(berlin_local, well_connected) | Count: 2907 | Prob: 0.2525
...
```

## Integration with Simulation Engine

The analysis output provides multiple approaches to improve the simulation engine's person generation:

### Approach 1: Update Existing Correlation Model
Use basic analysis output to improve the current correlation-based generation:
1. **Replace frequencies**: Use empirical marginal probabilities
2. **Update correlations**: Use observed pairwise correlations  
3. **Keep existing generation logic**: Maintain current multivariate normal approach

### Approach 2: Empirical Distribution Model (Recommended)
Use `--predict-types` output for data-driven generation that exactly matches observed distributions:

1. **Replace entire `generate_person()` method**: Use the generated code snippet
2. **Benefits**: 
   - Captures exact person type combinations seen in data
   - Handles complex multi-attribute interactions automatically
   - No assumptions about attribute independence or correlation structure
3. **Drawbacks**: 
   - Only generates person types that were observed in data collection
   - May need larger data collection for rare person types

#### Example Generated Code:
```python
def generate_person(self):
    """Generate person using empirical distribution"""
    import numpy as np
    
    types_and_probs = [
        ({'young': False, 'well_dressed': False}, 0.501019),
        ({'young': False, 'well_dressed': True}, 0.182721),
        # ... more types
    ]
    
    types = [tp[0] for tp in types_and_probs]
    probs = [tp[1] for tp in types_and_probs]
    selected_attrs = np.random.choice(len(types), p=probs)
    
    return {"attributes": types[selected_attrs]}
```

## Example Workflows

### Basic Workflow (Correlation-based improvements)
```bash
# 1. Collect data for Scenario 1
python data/collect_data.py 1 --runs 10

# 2. Analyze the collected data
python data/analyze_data.py 1 --save-results

# 3. Update simulation engine with new frequencies/correlations
# 4. Test with local simulation
python run_local_simulation.py
```

### Advanced Workflow (Empirical distribution modeling)
```bash
# 1. Collect comprehensive data for Scenario 2
python data/collect_data.py 2 --runs 20

# 2. Analyze with person type prediction
python data/analyze_data.py 2 --predict-types --save-results

# 3. Copy the generated generate_person() code into simulation engine
# 4. Test the empirical distribution model
python run_local_simulation.py

# 5. Compare results with original model
```

## Person Type Prediction Deep Dive

The `--predict-types` feature analyzes your collected data to discover the actual distribution of person types that the Berghain Challenge API generates. This goes beyond simple attribute correlations to capture the exact combinations of attributes that appear together.

### What It Does
1. **Discovers Person Types**: Finds all unique combinations of attributes in your data
2. **Calculates Frequencies**: Determines how often each person type appears
3. **Generates Samples**: Shows examples of persons the model would generate
4. **Provides Code**: Creates ready-to-use simulation code

### When To Use
- **For realistic simulations**: When you want your local simulation to generate the same person types as the real API
- **For rare combinations**: When you need to understand uncommon attribute patterns
- **For validation**: To verify your simulation matches real API behavior

### Key Benefits
- **No assumptions needed**: Doesn't assume attribute independence or specific correlation structures
- **Captures reality**: Uses actual observed person types rather than theoretical models
- **Easy integration**: Generates drop-in replacement code for simulation engine

### Limitations
- **Only observed types**: Can only generate person types that were seen during data collection
- **Requires sufficient data**: Rare person types need large datasets to be captured
- **Static model**: Doesn't generalize beyond the collected data

### Best Practices
- Collect data from multiple runs to capture API variability
- Use at least 15-20 runs for stable person type distributions  
- Review the person type output to ensure all expected combinations are present
- Consider hybrid approaches for scenarios with many rare person types

## Data Quality Notes

- **Sample Size**: Aim for at least 10,000+ people per scenario for reliable statistics
- **Multiple Runs**: Use multiple runs to account for API variability
- **Rate Limiting**: Built-in delays prevent overwhelming the API
- **Error Handling**: Automatic retry logic for transient failures

## Troubleshooting

- **Missing Data Files**: Run data collection first if analysis fails
- **API Errors**: Check environment variables and network connectivity
- **Large Files**: CSV files can be large (>1MB) for comprehensive data collection
- **Memory Issues**: For very large datasets, consider processing in chunks

## Environment Requirements

Ensure these environment variables are set:
- `BASE_URL`: API endpoint URL
- `PLAYER_ID`: Your player identifier

Load them from a `.env` file in the project root.
