#!/usr/bin/env python3
"""
Test script for tennis scoreboard system.
Simulates various scoring scenarios to verify functionality.
"""

import time
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.match import Match
from core.persistence import PersistenceManager
from ui.console_ui import ConsoleUI


def test_basic_scoring():
    """Test basic point scoring."""
    print("Testing basic point scoring...")
    
    match = Match()
    ui = ConsoleUI()
    match.attach(ui)
    
    # Test initial state
    print("Initial state:")
    ui.update(match.get_state())
    time.sleep(1)
    
    # Test home scoring
    print("\nHome scores a point...")
    match.home_scores_point()
    time.sleep(1)
    
    print("Home scores another point...")
    match.home_scores_point()
    time.sleep(1)
    
    print("Away scores a point...")
    match.away_scores_point()
    time.sleep(1)
    
    print("Home scores to win game...")
    match.home_scores_point()
    match.home_scores_point()
    time.sleep(1)
    
    print("Basic scoring test complete!")


def test_deuce_scenario():
    """Test deuce and advantage scenarios."""
    print("\nTesting deuce and advantage...")
    
    match = Match()
    ui = ConsoleUI()
    match.attach(ui)
    
    # Get to deuce (40-40)
    print("Getting to deuce...")
    for _ in range(3):
        match.home_scores_point()
        match.away_scores_point()
    
    ui.update(match.get_state())
    time.sleep(1)
    
    # Test advantage
    print("Home gets advantage...")
    match.home_scores_point()
    time.sleep(1)
    
    print("Away gets back to deuce...")
    match.away_scores_point()
    time.sleep(1)
    
    print("Home wins game...")
    match.home_scores_point()
    match.home_scores_point()
    time.sleep(1)
    
    print("Deuce test complete!")


def test_persistence():
    """Test persistence functionality."""
    print("\nTesting persistence...")
    
    match = Match()
    persistence = PersistenceManager("~/test_matches")
    
    # Score some points
    match.home_scores_point()
    match.home_scores_point()
    match.away_scores_point()
    
    # Save match
    filename = persistence.save_match(match.to_dict())
    print(f"Match saved to: {filename}")
    
    # Create new match
    new_match = Match()
    new_match.from_dict(match.to_dict())
    
    print("Match loaded from persistence:")
    print(f"  Sets: {new_match.sets}")
    print(f"  Games: {new_match.games}")
    print(f"  Points: {new_match.points}")
    
    # Clean up test directory
    import shutil
    shutil.rmtree("~/test_matches", ignore_errors=True)
    
    print("Persistence test complete!")


def test_input_simulation():
    """Test input handling simulation."""
    print("\nTesting input simulation...")
    
    from core.input import InputHandler
    
    match = Match()
    ui = ConsoleUI()
    match.attach(ui)
    
    input_handler = InputHandler()
    
    # Set up action handlers
    def home_point():
        match.home_scores_point()
        ui.update(match.get_state())
    
    def away_point():
        match.away_scores_point()
        ui.update(match.get_state())
    
    input_handler.set_action_handlers({
        'home_point': home_point,
        'away_point': away_point
    })
    
    # Simulate some inputs
    print("Simulating UP arrow (home point)...")
    input_handler.simulate_key_press('KEY_UP')
    time.sleep(1)
    
    print("Simulating DOWN arrow (away point)...")
    input_handler.simulate_key_press('KEY_DOWN')
    time.sleep(1)
    
    print("Simulating UP arrow again...")
    input_handler.simulate_key_press('KEY_UP')
    time.sleep(1)
    
    print("Input simulation test complete!")


def main():
    """Run all tests."""
    print("Tennis Scoreboard Test Suite")
    print("============================")
    print()
    
    try:
        test_basic_scoring()
        test_deuce_scenario()
        test_persistence()
        test_input_simulation()
        
        print("\nAll tests completed successfully!")
        print("The tennis scoreboard system is working correctly.")
        
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
