#!/usr/bin/env python3
"""
Simple test script to create a tournament
"""

import requests
import json
from datetime import datetime, timedelta

# API base URL
BASE_URL = "http://localhost:8000"

def create_tournament():
    """Create a tournament with admin credentials"""
    
    # Admin credentials (you'll need to create this user first)
    admin_email = "admin@test.com"
    admin_password = "testpassword123"
    
    print("🔐 Logging in as admin...")
    
    # Login to get access token
    login_data = {
        "username": admin_email,
        "password": admin_password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            print("💡 Make sure to run the full test first to create the admin user")
            return None
        
        token_data = response.json()
        access_token = token_data["access_token"]
        print("✅ Login successful")
        return access_token
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the FastAPI server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def post_tournament(access_token):
    """Post a new tournament"""
    
    # Tournament data
    tomorrow = datetime.now() + timedelta(days=1)
    
    tournament_data = {
        "name": "FNDC Championship 2024",
        "date": tomorrow.isoformat(),
        "location": "Centro de Convenciones",
        "start_time": "15:00",
        "duration_days": 3,
        "rounds": 8
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print("🏆 Creating tournament...")
    print(f"   Name: {tournament_data['name']}")
    print(f"   Date: {tournament_data['date']}")
    print(f"   Location: {tournament_data['location']}")
    
    try:
        response = requests.post(f"{BASE_URL}/tournaments/", json=tournament_data, headers=headers)
        
        if response.status_code == 200:
            tournament = response.json()
            print("✅ Tournament created successfully!")
            print(f"   Tournament ID: {tournament['id']}")
            print(f"   Created by: {tournament['created_by']}")
            return tournament
        else:
            print(f"❌ Tournament creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Tournament creation error: {e}")
        return None

if __name__ == "__main__":
    print("🚀 Simple Tournament Creation Test")
    print("=" * 40)
    
    # Get access token
    access_token = create_tournament()
    
    if access_token:
        # Create tournament
        tournament = post_tournament(access_token)
        
        if tournament:
            print("\n🎉 Success! Tournament created and saved to database.")
            print(f"   You can now view it in the API docs: http://localhost:8000/docs")
    
    print("\n" + "=" * 40)
    print("🏁 Test completed!") 