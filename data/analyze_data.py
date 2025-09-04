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
        print(f"  P(young={young}, well_dressed={well_dressed}) = {prob:.4f}")
    
    # Calculate marginal probabilities
    young_prob = df['young'].mean()
    well_dressed_prob = df['well_dressed'].mean()
    
    print(f"\nMarginal Probabilities:")
    print(f"  P(young=True) = {young_prob:.4f}")
    print(f"  P(well_dressed=True) = {well_dressed_prob:.4f}")
    
    # Calculate and verify correlation
    correlation = df['young'].corr(df['well_dressed'])
    print(f"\nObserved Correlation:")
    print(f"  corr(young, well_dressed) = {correlation:.4f}")
    
    # Compare with independence assumption
    independent_joint = young_prob * well_dressed_prob
    observed_joint = joint_probs.get((True, True), 0)
    
    print(f"\nIndependence Check:")
    print(f"  P(both | independent) = {independent_joint:.4f}")
    print(f"  P(both | observed) = {observed_joint:.4f}")
    print(f"  Ratio = {observed_joint/independent_joint:.2f}" if independent_joint > 0 else "  Ratio = N/A")
    
    # Generate code for simulation engine
    print(f"\n=== SIMULATION ENGINE CODE ===")
    print("Replace generate_person() method with:")
    print("""
def generate_person(self):
    \"\"\"Generate person using empirical joint distribution\"\"\"
    joint_probs = {""")
    
    for (young, well_dressed), prob in joint_probs.items():
        print(f"        ({young}, {well_dressed}): {prob:.6f},")
    
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
        print(f"  P({attr}=True) = {prob:.4f}")
    
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
        print(f"  corr({attr1}, {attr2}) = {corr:.4f}")
    
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
                
                print(f"    P({target_attr}=True | {cond_attr}=True) = {prob_given_true:.4f}")
                print(f"    P({target_attr}=True | {cond_attr}=False) = {prob_given_false:.4f}")
    
    # Print simulation engine update
    print(f"\n=== SIMULATION ENGINE UPDATES ===")
    print(f"Update scenario {scenario} frequencies and correlations:")
    print("\n# Frequencies:")
    for attr, freq in marginals.items():
        print(f"'{attr}': {freq:.6f},")
    
    print("\n# Correlations:")
    for attr1 in attribute_cols:
        print(f"'{attr1}': {{")
        for attr2 in attribute_cols:
            corr_val = correlations.get(attr1, {}).get(attr2, 0.0)
            print(f"    '{attr2}': {corr_val:.6f},")
        print("},")
    
    return {
        'marginal_probabilities': marginals,
        'correlations': correlations,
        'conditional_probabilities': conditional_probs,
        'total_samples': len(df)
    }

def main():
    parser = argparse.ArgumentParser(description='Analyze collected Berghain Challenge data')
    parser.add_argument('scenario', type=int, choices=[1, 2, 3],
                       help='Scenario to analyze (1, 2, or 3)')
    parser.add_argument('--save-results', action='store_true',
                       help='Save analysis results to JSON file')
    
    args = parser.parse_args()
    
    csv_file = f"scenario_{args.scenario}_people_data.csv"
    
    if args.scenario == 1:
        results = analyze_scenario_1_data(csv_file)
    else:
        results = analyze_complex_scenario_data(csv_file, args.scenario)
    
    if results and args.save_results:
        output_file = f"scenario_{args.scenario}_analysis.json"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()