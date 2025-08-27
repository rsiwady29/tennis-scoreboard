#!/usr/bin/env python3
"""
Debug script to test tiebreak logic step by step.
"""

import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.match import Match


def debug_tiebreak():
    """Debug the tiebreak logic step by step."""
    print("Debugging Tiebreak Logic")
    print("=" * 40)
    print()
    
    match = Match()
    
    print("Initial state:")
    print(f"  Games: {match.games}")
    print(f"  Points: {match.points}")
    print(f"  In tiebreak: {match.in_tiebreak}")
    print(f"  Tiebreak points: {match.tiebreak_points}")
    print()
    
    # Get both players to 6-6 games
    print("Getting both players to 6-6 games...")
    
    # Home wins 6 games
    for i in range(6):
        print(f"Home wins game {i+1}...")
        for _ in range(4):
            match.home_scores_point()
        print(f"  Games: {match.games}")
        print(f"  In tiebreak: {match.in_tiebreak}")
        print()
    
    # Away wins 6 games
    for i in range(6):
        print(f"Away wins game {i+1}...")
        for _ in range(4):
            match.away_scores_point()
        print(f"  Games: {match.games}")
        print(f"  In tiebreak: {match.in_tiebreak}")
        print()
    
    print("After both players reach 6-6:")
    print(f"  Games: {match.games}")
    print(f"  Points: {match.points}")
    print(f"  In tiebreak: {match.in_tiebreak}")
    print(f"  Tiebreak points: {match.tiebreak_points}")
    print()
    
    if match.in_tiebreak:
        print("✅ Tiebreak started correctly!")
        
        # Test tiebreak scoring
        print("Testing tiebreak scoring...")
        match.home_scores_point()
        print(f"  Home scores: {match.tiebreak_points}")
        
        match.away_scores_point()
        print(f"  Away scores: {match.tiebreak_points}")
        
        match.home_scores_point()
        print(f"  Home scores again: {match.tiebreak_points}")
        
    else:
        print("❌ Tiebreak did NOT start!")
        print("This indicates a bug in the logic.")


if __name__ == "__main__":
    debug_tiebreak()
