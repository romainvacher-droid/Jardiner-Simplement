#!/usr/bin/env python3
"""
Test script for the authentication system.
"""

import sys
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, '.')

from utils.auth import (
    create_user,
    user_exists,
    authenticate_user,
    login_user,
    logout_user,
    load_user_data,
    update_user_favorites,
    update_user_garden,
    get_current_user,
    is_authenticated
)

def test_auth_system():
    """Test the authentication system."""
    print("=" * 60)
    print("Testing Authentication System")
    print("=" * 60)
    
    # Test 1: Create a test user
    print("\n1. Creating test user 'testuser'...")
    success = create_user("testuser", "testpass123")
    if success:
        print("   [OK] User created successfully")
    else:
        print("   [FAIL] Failed to create user (might already exist)")
    
    # Test 2: Check if user exists
    print("\n2. Checking if user exists...")
    exists = user_exists("testuser")
    print(f"   User exists: {exists}")
    
    # Test 3: Authenticate user
    print("\n3. Authenticating user...")
    auth = authenticate_user("testuser", "testpass123")
    print(f"   Authentication result: {auth}")
    
    # Test 4: Load user data
    print("\n4. Loading user data...")
    user_data = load_user_data("testuser")
    if user_data:
        print(f"   [OK] User data loaded:")
        print(f"      - Username: {user_data['username']}")
        print(f"      - Favorites: {user_data['favorites']}")
        print(f"      - Garden plants: {len(user_data['mon_jardin'])}")
    else:
        print("   [FAIL] Failed to load user data")
    
    # Test 5: Update favorites
    print("\n5. Updating favorites...")
    test_favorites = {
        "legumes": ["Tomate", "Carotte"],
        "associations": [{"plante1": "Tomate 🍅", "plante2": "Basilic 🌿"}],
        "nuisibles": ["Pucerons"]
    }
    update_success = update_user_favorites("testuser", test_favorites)
    print(f"   Update success: {update_success}")
    
    # Verify update
    user_data = load_user_data("testuser")
    print(f"   Updated favorites: {user_data['favorites']}")
    
    # Test 6: Update garden
    print("\n6. Updating garden...")
    test_garden = [
        {
            "legume": "Tomate",
            "date_plantation": "2024-05-15",
            "quantite": 5,
            "emoji": "🍅"
        }
    ]
    garden_success = update_user_garden("testuser", test_garden)
    print(f"   Garden update success: {garden_success}")
    
    # Verify garden update
    user_data = load_user_data("testuser")
    print(f"   Updated garden: {len(user_data['mon_jardin'])} plants")
    
    # Test 7: Simulate login (session state)
    print("\n7. Simulating login (session state)...")
    # We can't test Streamlit session state outside of Streamlit,
    # but we can test the login_user function logic
    print("   (Skipping session state test - requires Streamlit context)")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
    
    # Show user file location
    user_file = Path("users/testuser.json")
    if user_file.exists():
        print(f"\nUser file created at: {user_file.absolute()}")
        print("\nFile contents:")
        print("-" * 40)
        with open(user_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            print(json.dumps(content, indent=2, ensure_ascii=False))
        print("-" * 40)

if __name__ == "__main__":
    test_auth_system()