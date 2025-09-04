#!/usr/bin/env python3
"""
Data Collection Script for Berghain Challenge

This script runs multiple games using a simple "reject 19, select 1" algorithm
to maximize the number of people we see and collect distribution data.
"""

import urllib.request
import json
import time
import os
import argparse
import csv
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BASE_URL = os.getenv("BASE_URL")
PLAYER_ID = os.getenv("PLAYER_ID")

# Game Settings
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1

class SimpleDataCollector:
    """Simple bouncer that rejects 19 people then selects 1 to maximize data collection"""
    
    def __init__(self, scenario, verbose=True):
        self.scenario = scenario
        self.verbose = verbose
        self.game_id = None
        self.people_count = 0
        self.admitted_count = 0
        self.rejected_count = 0
        
        # Data collection setup
        self.data_file = f"scenario_{scenario}_people_data.csv"
        self.run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.getpid()}"
        
    def log_person(self, person_index, attributes, decision):
        """Log each person seen during the game"""
        file_exists = os.path.exists(self.data_file)
        
        with open(self.data_file, 'a', newline='') as f:
            writer = csv.writer(f)
            
            if not file_exists:
                header = ['run_id', 'game_id', 'person_index', 'decision'] + sorted(attributes.keys())
                writer.writerow(header)
            
            row = [self.run_id, self.game_id, person_index, decision] + [attributes.get(attr, False) for attr in sorted(attributes.keys())]
            writer.writerow(row)
    
    
    def start_new_game(self):
        """Start a new game via API"""
        if self.verbose:
            print(f"Starting new game for scenario {self.scenario}...")
        
        url = f"{BASE_URL}/new-game?scenario={self.scenario}&playerId={PLAYER_ID}"
        try:
            req = urllib.request.Request(url, method='POST')
            with urllib.request.urlopen(req) as response:
                if response.status < 200 or response.status >= 300:
                    raise urllib.error.HTTPError(url, response.status, response.reason, response.headers, response.fp)
                game_data = json.loads(response.read().decode('utf-8'))

            self.game_id = game_data['gameId']
            
            if self.verbose:
                print(f"Game {self.game_id} started.")
            return game_data
        except Exception as e:
            if self.verbose:
                print(f"Error starting game: {e}")
            return None

    def get_next_person(self, person_index, accept=None):
        """Get next person from API with retry logic"""
        url = f"{BASE_URL}/decide-and-next?gameId={self.game_id}&personIndex={person_index}"
        if accept is not None:
            url += f"&accept={str(accept).lower()}"
        
        for attempt in range(RETRY_ATTEMPTS):
            try:
                req = urllib.request.Request(url, method='POST')
                with urllib.request.urlopen(req) as response:
                    if response.status < 200 or response.status >= 300:
                        raise urllib.error.HTTPError(url, response.status, response.reason, response.headers, response.fp)
                    return json.loads(response.read().decode('utf-8'))
            except urllib.error.HTTPError as e:
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

    def make_decision(self, person):
        """Simple algorithm: reject 19 people, then select 1"""
        # Reject 19 people, then accept 1 (cycle of 20)
        decision = (self.people_count % 20) == 19
        return decision

    def run_game(self):
        """Run the main game loop with simple reject-19-select-1 algorithm"""
        if not self.start_new_game():
            return False

        # Get first person
        result = self.get_next_person(person_index=0)
        if not result or not result.get('nextPerson'):
            print("Failed to get the first person.")
            return False

        next_person = result.get('nextPerson')

        # Main game loop
        while result.get('status') == 'running' and next_person:
            self.people_count += 1
            
            # Make decision using simple algorithm
            decision = self.make_decision(next_person)
            
            # Log the person data
            self.log_person(next_person['personIndex'], next_person['attributes'], decision)
            
            if self.verbose and self.people_count % 1000 == 0:
                print(f"  Processed {self.people_count} people, admitted {self.admitted_count}")
            
            # Submit decision and get next person
            result = self.get_next_person(person_index=next_person['personIndex'], accept=decision)

            if not result:
                if self.verbose:
                    print("Failed to get next person. Ending game.")
                break

            # Update counters
            if decision:
                self.admitted_count += 1
            else:
                self.rejected_count += 1

            next_person = result.get('nextPerson')
            time.sleep(0.01)  # Small delay to not overwhelm API

        # Game end
        if result and result.get('status') == 'completed':
            final_stats = {
                'status': 'completed',
                'people_seen': self.people_count,
                'admitted_count': self.admitted_count,
                'rejected_count': result['rejectedCount']
            }
            
            if self.verbose:
                print("--- GAME COMPLETED ---")
                print(f"People seen: {self.people_count}")
                print(f"Final Admitted: {self.admitted_count}")
                print(f"Final Rejected: {result['rejectedCount']}")
            return True
        elif result and result.get('status') == 'failed':
            final_stats = {
                'status': 'failed',
                'reason': result.get('reason'),
                'people_seen': self.people_count,
                'admitted_count': self.admitted_count,
                'rejected_count': self.rejected_count
            }
            
            if self.verbose:
                print("--- GAME FAILED ---")
                print(f"Reason: {result.get('reason')}")
                print(f"People seen: {self.people_count}")
            return False
        
        return False

def run_data_collection(scenario, num_runs=5, delay_between_runs=30):
    """
    Run multiple data collection sessions for a given scenario
    
    Args:
        scenario: Scenario number (1, 2, or 3)
        num_runs: Number of games to run for data collection
        delay_between_runs: Seconds to wait between runs (for rate limiting)
    """
    print(f"\n=== Starting Data Collection for Scenario {scenario} ===")
    print(f"Using simple 'reject 19, select 1' algorithm to maximize data collection")
    print(f"Planning to run {num_runs} games with {delay_between_runs}s delays")
    
    for run_num in range(1, num_runs + 1):
        print(f"\n--- Run {run_num}/{num_runs} for Scenario {scenario} ---")
        
        try:
            collector = SimpleDataCollector(scenario, verbose=True)
            success = collector.run_game()
            
            if success:
                print(f"✓ Run {run_num} completed successfully")
                print(f"  People seen: {collector.people_count}")
                print(f"  Final admitted: {collector.admitted_count}")
                print(f"  Data collected in: {collector.data_file}")
                print(f"  Run ID: {collector.run_id}")
            else:
                print(f"✗ Run {run_num} failed")
                    
        except Exception as e:
            print(f"✗ Run {run_num} failed with exception: {e}")
        
        # Wait between runs (except for the last one)
        if run_num < num_runs:
            print(f"  Waiting {delay_between_runs}s before next run...")
            time.sleep(delay_between_runs)
    
    print(f"\n=== Data Collection Complete for Scenario {scenario} ===")
    print(f"Check scenario_{scenario}_people_data.csv for collected data")

def main():
    parser = argparse.ArgumentParser(description='Collect distribution data from Berghain Challenge API')
    parser.add_argument('scenario', type=int, choices=[1, 2, 3], 
                       help='Scenario to collect data for (1, 2, or 3)')
    parser.add_argument('--runs', type=int, default=5,
                       help='Number of games to run (default: 5)')
    parser.add_argument('--delay', type=int, default=30,
                       help='Seconds to wait between runs (default: 30)')
    parser.add_argument('--all', action='store_true',
                       help='Collect data for all scenarios sequentially')
    
    args = parser.parse_args()
    
    if args.all:
        # Run all scenarios
        for scenario in [1, 2, 3]:
            run_data_collection(scenario, args.runs, args.delay)
            if scenario < 3:  # Extra delay between scenarios
                print(f"\nWaiting {args.delay * 2}s before next scenario...")
                time.sleep(args.delay * 2)
    else:
        # Run single scenario
        run_data_collection(args.scenario, args.runs, args.delay)

if __name__ == "__main__":
    main()