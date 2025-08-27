#!/usr/bin/env python3
"""
Test script to demonstrate tiebreak functionality in tennis scoring.
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.match import Match


def test_tiebreak_scenario():
    """Test a complete tiebreak scenario."""
    print("Testing Tiebreak Scenario")
    print("=" * 40)
    print()
    
    match = Match()
    
    print("Starting match...")
    print(f"Initial state: Sets {match.sets}, Games {match.games}, Points {match.points}")
    print()
    
    # Get both players to 6-6 games
    print("Getting both players to 6-6 games...")
    
    # Home wins 6 games
    for _ in range(6):
        match.home_scores_point()
        match.home_scores_point()
        match.home_scores_point()
        match.home_scores_point()
    
    # Away wins 6 games
    for _ in range(6):
        match.away_scores_point()
        match.away_scores_point()
        match.away_scores_point()
        match.away_scores_point()
    
    print(f"Games: {match.games}")
    print(f"Tiebreak should start: {match.in_tiebreak}")
    print()
    
    if match.in_tiebreak:
        print("TIEBREAK STARTED!")
        print("Now scoring tiebreak points...")
        print()
        
        # Score some tiebreak points
        print("Home scores 2 tiebreak points...")
        match.home_scores_point()  # 1-0
        match.home_scores_point()  # 2-0
        
        print(f"Tiebreak score: {match.tiebreak_points}")
        print()
        
        print("Away scores 3 tiebreak points...")
        match.away_scores_point()  # 2-1
        match.away_scores_point()  # 2-2
        match.away_scores_point()  # 2-3
        
        print(f"Tiebreak score: {match.tiebreak_points}")
        print()
        
        print("Home scores to 7-3 to win tiebreak...")
        for _ in range(5):
            match.home_scores_point()
        
        print(f"Final tiebreak score: {match.tiebreak_points}")
        print(f"Set won: {match.sets}")
        print(f"Tiebreak ended: {not match.in_tiebreak}")
        print()
        
        if match.sets[0] == 1:
            print("✅ Tiebreak test PASSED! Home won the set via tiebreak.")
        else:
            print("❌ Tiebreak test FAILED! Set not won correctly.")
    else:
        print("❌ Tiebreak test FAILED! Tiebreak did not start at 6-6.")
    
    print()
    print("Test completed.")


def test_tiebreak_edge_cases():
    """Test tiebreak edge cases like 7-5, 8-6, etc."""
    print("Testing Tiebreak Edge Cases")
    print("=" * 40)
    print()
    
    match = Match()
    
    # Get to 6-6 games
    for _ in range(6):
        match.home_scores_point()
        match.home_scores_point()
        match.home_scores_point()
        match.home_scores_point()
    
    for _ in range(6):
        match.away_scores_point()
        match.away_scores_point()
        match.away_scores_point()
        match.away_scores_point()
    
    print("Testing 7-5 tiebreak win...")
    
    # Home gets to 7, Away stays at 5
    for _ in range(7):
        match.home_scores_point()
    
    for _ in range(5):
        match.away_scores_point()
    
    print(f"Tiebreak score: {match.tiebreak_points}")
    print(f"Set won: {match.sets}")
    
    if match.sets[0] == 1:
        print("✅ 7-5 tiebreak test PASSED!")
    else:
        print("❌ 7-5 tiebreak test FAILED!")
    
    print()
    
    # Test 8-6 scenario (must win by 2)
    print("Testing 8-6 tiebreak scenario...")
    match.reset()
    
    # Get to 6-6 games again
    for _ in range(6):
        match.home_scores_point()
        match.home_scores_point()
        match.home_scores_point()
        match.home_scores_point()
    
    for _ in range(6):
        match.away_scores_point()
        match.away_scores_point()
        match.away_scores_point()
        match.away_scores_point()
    
    # Both get to 6-6 in tiebreak
    for _ in range(6):
        match.home_scores_point()
        match.away_scores_point()
    
    print(f"Tiebreak at 6-6: {match.tiebreak_points}")
    
    # Home wins next 2 points to win 8-6
    match.home_scores_point()  # 7-6
    match.home_scores_point()  # 8-6
    
    print(f"Final tiebreak score: {match.tiebreak_points}")
    print(f"Set won: {match.sets}")
    
    if match.sets[0] == 1:
        print("✅ 8-6 tiebreak test PASSED!")
    else:
        print("❌ 8-6 tiebreak test FAILED!")
    
    print()
    print("Edge case tests completed.")


def main():
    """Run all tiebreak tests."""
    print("Tennis Tiebreak Test Suite")
    print("=" * 50)
    print()
    
    try:
        test_tiebreak_scenario()
        print()
        test_tiebreak_edge_cases()
        
        print("\n🎾 All tiebreak tests completed!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
