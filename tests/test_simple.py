#!/usr/bin/env python3
"""
Simple test to verify console output works correctly.
"""

import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    
    print("=" * 60)
    print("SIMPLE TEST")
    print("=" * 60)
    print()
    
    print("SCORE:")
    print("------")
    print("Sets:   Home 0 - Away 0")
    print("Games:  Home 0 - Away 0")
    print("Points: 0 - 0")
    print()
    
    print("SERVER:")
    print("-------")
    print("Current: Home")
    print()
    
    print("MATCH STATUS:")
    print("-------------")
    print("IN PROGRESS")
    print()
    
    print("CONTROLS:")
    print("----------")
    print("UP Arrow    - Home scores point")
    print("DOWN Arrow  - Away scores point")
    print()
    
    print("-" * 60)
    print("Press Ctrl+C to exit")
    print("-" * 60)
    
    # Wait a bit
    time.sleep(3)
    
    print("\n>>> Test message")
    time.sleep(1)
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    main()
