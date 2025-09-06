#!/usr/bin/env python3
"""
Data Analysis Script for Berghain Challenge

Analyzes collected distribution data to build empirical models
that can replace the independent probability generation.
"""

import pandas as pd
import numpy as np
import json
import argparse
from itertools import combinations
import os
from collections import Counter

def analyze_scenario_1_data(csv_file):
    """
    Analyze Scenario 1 data to build exact joint probability table
    
    Args:
        csv_file: Path to the collected data CSV
        
    Returns:
        Dictionary with joint probabilities and analysis
    """
    if not os.path.exists(csv_file):
        print(f"Data file {csv_file} not found. Run data collection first.")
        return None
        
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} records from {csv_file}")
    
    # Calculate joint probabilities
    joint_counts = df.groupby(['young', 'well_dressed']).size()
    total = len(df)
    joint_probs = joint_counts / total
    
    print("\n=== SCENARIO 1 JOINT DISTRIBUTION ===")
    print("Joint Probabilities:")
    for (young, well_dressed), prob in joint_probs.items():
        print(f"  P(young={young}, well_dressed={well_dressed}) = {prob}")
    
    # Calculate marginal probabilities
    young_prob = df['young'].mean()
    well_dressed_prob = df['well_dressed'].mean()
    
    print(f"\nMarginal Probabilities:")
    print(f"  P(young=True) = {young_prob}")
    print(f"  P(well_dressed=True) = {well_dressed_prob}")
    
    # Calculate and verify correlation
    correlation = df['young'].corr(df['well_dressed'])
    print(f"\nObserved Correlation:")
    print(f"  corr(young, well_dressed) = {correlation}")
    
    # Compare with independence assumption
    independent_joint = young_prob * well_dressed_prob
    observed_joint = joint_probs.get((True, True), 0)
    
    print(f"\nIndependence Check:")
    print(f"  P(both | independent) = {independent_joint}")
    print(f"  P(both | observed) = {observed_joint}")
    print(f"  Ratio = {observed_joint/independent_joint}" if independent_joint > 0 else "  Ratio = N/A")
    
    # Generate code for simulation engine
    print(f"\n=== SIMULATION ENGINE CODE ===")
    print("Replace generate_person() method with:")
    print("""
def generate_person(self):
    \"\"\"Generate person using empirical joint distribution\"\"\"
    joint_probs = {""")
    
    for (young, well_dressed), prob in joint_probs.items():
        print(f"        ({young}, {well_dressed}): {prob},")
    
    print("""    }
    
    rand = random.random()
    cumsum = 0
    for (young, well_dressed), prob in joint_probs.items():
        cumsum += prob
        if rand <= cumsum:
            return {
                'attributes': {
                    'young': young,
                    'well_dressed': well_dressed
                }
            }
    
    # Fallback (should never reach here)
    return {'attributes': {'young': False, 'well_dressed': False}}
""")
    
    return {
        'joint_probabilities': joint_probs.to_dict(),
        'marginal_probabilities': {'young': young_prob, 'well_dressed': well_dressed_prob},
        'correlation': correlation,
        'total_samples': total
    }

def analyze_complex_scenario_data(csv_file, scenario):
    """
    Analyze complex scenario data to build conditional probability models
    
    Args:
        csv_file: Path to the collected data CSV
        scenario: Scenario number (2 or 3)
        
    Returns:
        Dictionary with conditional probabilities and analysis
    """
    if not os.path.exists(csv_file):
        print(f"Data file {csv_file} not found. Run data collection first.")
        return None
        
    df = pd.read_csv(csv_file)
    print(f"Loaded {len(df)} records from {csv_file}")
    
    # Get attribute columns (excluding metadata)
    attribute_cols = [col for col in df.columns if col not in ['run_id', 'game_id', 'person_index', 'decision']]
    
    print(f"\n=== SCENARIO {scenario} DISTRIBUTION ANALYSIS ===")
    
    # Calculate marginal probabilities
    marginals = {}
    print("Marginal Probabilities:")
    for attr in attribute_cols:
        prob = df[attr].mean()
        marginals[attr] = prob
        print(f"  P({attr}=True) = {prob}")
    
    # Calculate pairwise correlations
    print(f"\nPairwise Correlations:")
    correlations = {}
    for attr1, attr2 in combinations(attribute_cols, 2):
        corr = df[attr1].corr(df[attr2])
        if attr1 not in correlations:
            correlations[attr1] = {}
        if attr2 not in correlations:
            correlations[attr2] = {}
        correlations[attr1][attr2] = corr
        correlations[attr2][attr1] = corr
        print(f"  corr({attr1}, {attr2}) = {corr}")
    
    # Add self-correlations
    for attr in attribute_cols:
        if attr not in correlations:
            correlations[attr] = {}
        correlations[attr][attr] = 1.0
    
    # Calculate conditional probabilities
    print(f"\nConditional Probabilities:")
    conditional_probs = {}
    
    for target_attr in attribute_cols:
        conditional_probs[target_attr] = {}
        print(f"\n  For {target_attr}:")
        
        for cond_attr in attribute_cols:
            if cond_attr != target_attr:
                # P(target=True | cond=True)
                cond_true_data = df[df[cond_attr] == True]
                cond_false_data = df[df[cond_attr] == False]
                
                prob_given_true = cond_true_data[target_attr].mean() if len(cond_true_data) > 0 else marginals[target_attr]
                prob_given_false = cond_false_data[target_attr].mean() if len(cond_false_data) > 0 else marginals[target_attr]
                
                conditional_probs[target_attr][cond_attr] = {
                    'given_true': prob_given_true,
                    'given_false': prob_given_false
                }
                
                print(f"    P({target_attr}=True | {cond_attr}=True) = {prob_given_true}")
                print(f"    P({target_attr}=True | {cond_attr}=False) = {prob_given_false}")
    
    # Print simulation engine update
    print(f"\n=== SIMULATION ENGINE UPDATES ===")
    print(f"Update scenario {scenario} frequencies and correlations:")
    print("\n# Frequencies:")
    for attr, freq in marginals.items():
        print(f"'{attr}': {freq},")
    
    print("\n# Correlations:")
    for attr1 in attribute_cols:
        print(f"'{attr1}': {{")
        for attr2 in attribute_cols:
            corr_val = correlations.get(attr1, {}).get(attr2, 0.0)
            print(f"    '{attr2}': {corr_val},")
        print("},")
    
    return {
        'marginal_probabilities': marginals,
        'correlations': correlations,
        'conditional_probabilities': conditional_probs,
        'total_samples': len(df)
    }

def predict_person_type_distribution(csv_file, scenario):
    """
    Analyze person type distributions and generate predictive capabilities
    
    Args:
        csv_file: Path to the collected data CSV
        scenario: Scenario number (1, 2, or 3)
        
    Returns:
        Dictionary with person type distributions and prediction functions
    """
    if not os.path.exists(csv_file):
        print(f"Data file {csv_file} not found. Run data collection first.")
        return None
        
    df = pd.read_csv(csv_file)
    print(f"\n=== SCENARIO {scenario} PERSON TYPE PREDICTION ==")
    print(f"Loaded {len(df)} records from {csv_file}")
    
    # Get attribute columns (excluding metadata)
    attribute_cols = [col for col in df.columns if col not in ['run_id', 'game_id', 'person_index', 'decision']]
    
    # Create person type combinations as tuples
    person_types = []
    for _, row in df.iterrows():
        person_type = tuple(row[attr] for attr in attribute_cols)
        person_types.append(person_type)
    
    # Count frequencies of each person type
    type_counts = Counter(person_types)
    total_people = len(person_types)
    
    # Calculate probabilities
    type_probabilities = {}
    for person_type, count in type_counts.items():
        type_probabilities[person_type] = count / total_people
    
    print(f"\nFound {len(type_counts)} unique person types:")
    print("Person Type Distribution:")
    
    # Sort by frequency for better readability
    sorted_types = sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
    
    for person_type, count in sorted_types:
        prob = type_probabilities[person_type]
        
        # Create readable description
        attrs_true = []
        attrs_false = []
        for i, attr in enumerate(attribute_cols):
            if person_type[i]:
                attrs_true.append(attr)
            else:
                attrs_false.append(f"¬{attr}")
        
        if attrs_true:
            description = f"({', '.join(attrs_true)})"
        else:
            description = f"({', '.join(attrs_false)})"
            
        print(f"  {description:40s} | Count: {count:4d} | Prob: {prob}")
    
    # Generate sample persons to demonstrate prediction
    print(f"\n=== SAMPLE PERSON GENERATION ===")
    print("Generating 10 sample persons using empirical distribution:")
    
    # Convert to lists for numpy choice
    types_list = list(type_probabilities.keys())
    probs_list = list(type_probabilities.values())
    
    # Generate samples
    np.random.seed(42)  # For reproducible results
    sample_indices = np.random.choice(len(types_list), size=10, p=probs_list)
    
    for i, idx in enumerate(sample_indices):
        person_type = types_list[idx]
        
        attrs_desc = []
        for j, attr in enumerate(attribute_cols):
            if person_type[j]:
                attrs_desc.append(attr)
        
        if attrs_desc:
            description = ', '.join(attrs_desc)
        else:
            description = 'no attributes'
            
        print(f"  Person {i+1:2d}: {description}")
    
    # Generate code for simulation engine
    print(f"\n=== SIMULATION CODE GENERATION ===")
    print(f"Updated generate_person() method for scenario {scenario}:")
    print('"""')
    print('def generate_person(self):')
    print('    """Generate person using empirical distribution"""')
    print('    import numpy as np')
    print('    ')
    print('    # Person type probabilities from data analysis')
    print('    types_and_probs = [')
    
    for person_type, prob in type_probabilities.items():
        attrs_dict = {attribute_cols[i]: person_type[i] for i in range(len(attribute_cols))}
        print(f'        ({attrs_dict}, {prob}),')
    
    print('    ]')
    print('    ')
    print('    # Sample person type')
    print('    types = [tp[0] for tp in types_and_probs]')
    print('    probs = [tp[1] for tp in types_and_probs]')
    print('    selected_idx = np.random.choice(len(types), p=probs)')
    print('    ')
    print('    return {"attributes": types[selected_idx]}')
    print('"""')
    
    return {
        'scenario': scenario,
        'attribute_columns': attribute_cols,
        'person_type_counts': dict(type_counts),
        'person_type_probabilities': type_probabilities,
        'total_samples': total_people,
        'unique_types': len(type_counts)
    }

def generate_predicted_person(type_probabilities, attribute_cols):
    """
    Generate a single person using the empirical distribution
    
    Args:
        type_probabilities: Dict mapping person types to probabilities
        attribute_cols: List of attribute column names
        
    Returns:
        Dict with person attributes
    """
    types_list = list(type_probabilities.keys())
    probs_list = list(type_probabilities.values())
    
    # Sample a person type
    selected_idx = np.random.choice(len(types_list), p=probs_list)
    selected_type = types_list[selected_idx]
    
    # Convert to attribute dictionary
    attributes = {attribute_cols[i]: selected_type[i] for i in range(len(attribute_cols))}
    
    return {'attributes': attributes}

def main():
    parser = argparse.ArgumentParser(description='Analyze collected Berghain Challenge data')
    parser.add_argument('scenario', type=int, choices=[1, 2, 3],
                       help='Scenario to analyze (1, 2, or 3)')
    parser.add_argument('--save-results', action='store_true',
                       help='Save analysis results to JSON file')
    parser.add_argument('--predict-types', action='store_true',
                       help='Analyze and predict person type distributions')
    
    args = parser.parse_args()
    
    # Try both relative paths - from data folder and from project root
    csv_file_local = f"scenario_{args.scenario}_people_data.csv"
    csv_file_from_root = f"data/scenario_{args.scenario}_people_data.csv"
    
    if os.path.exists(csv_file_local):
        csv_file = csv_file_local
    elif os.path.exists(csv_file_from_root):
        csv_file = csv_file_from_root
    else:
        csv_file = csv_file_local  # Use local path for error message
    
    # Run standard analysis
    if args.scenario == 1:
        results = analyze_scenario_1_data(csv_file)
    else:
        results = analyze_complex_scenario_data(csv_file, args.scenario)
    
    # Run prediction analysis if requested
    prediction_results = None
    if args.predict_types:
        prediction_results = predict_person_type_distribution(csv_file, args.scenario)
        if results and prediction_results:
            results['prediction_analysis'] = prediction_results
    
    # Save results
    if results and args.save_results:
        output_file = f"scenario_{args.scenario}_analysis.json"
        # Handle numpy types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=convert_numpy)
        print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()