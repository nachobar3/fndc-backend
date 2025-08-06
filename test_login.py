import requests
import json

baseurl = "http://localhost:8000"

def login_and_test_protected():
    """Login and test protected endpoints"""
    print("🔐 LOGIN AND PROTECTED ENDPOINTS TEST")
    print("=" * 50)
    
    # First, try to login with the test user we just created
    login_data = {
        "username": "test@example.com",
        "password": "test123456"
    }
    
    print("🔍 Attempting login...")
    try:
        response = requests.post(f"{baseurl}/auth/login", data=login_data, timeout=5)
        print(f"Login Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token")
            print(f"✅ Login successful! Token: {token[:20]}...")
            
            # Test protected endpoints with the token
            headers = {"Authorization": f"Bearer {token}"}
            
            print("\n🔒 Testing protected endpoints...")
            
            # Test user profile
            profile_response = requests.get(f"{baseurl}/auth/me", headers=headers, timeout=5)
            print(f"Profile Status: {profile_response.status_code}")
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print(f"✅ User Profile: {profile.get('name')} ({profile.get('email')})")
            
            # Test tournament registration
            reg_response = requests.post(f"{baseurl}/tournaments/689173a65550a20c74c67494/register", headers=headers, timeout=5)
            print(f"Registration Status: {reg_response.status_code}")
            if reg_response.status_code == 200:
                print("✅ Successfully registered to tournament!")
            else:
                print(f"❌ Registration failed: {reg_response.text}")
            
            # Test cube proposal
            cube_data = {
                "tournament_id": "689173a65550a20c74c67494",
                "cube_url": "https://cubecobra.com/cube/list/test",
                "description": "Test cube proposal from API test"
            }
            cube_response = requests.post(f"{baseurl}/cubes/propose", json=cube_data, headers=headers, timeout=5)
            print(f"Cube Proposal Status: {cube_response.status_code}")
            if cube_response.status_code == 200:
                print("✅ Successfully proposed cube!")
            else:
                print(f"❌ Cube proposal failed: {cube_response.text}")
                
        else:
            print(f"❌ Login failed: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

def test_admin_login():
    """Test admin login if we have admin credentials"""
    print("\n👑 ADMIN LOGIN TEST")
    print("=" * 50)
    
    # You would need to create an admin user first using create_admin.py
    # For now, we'll just show how it would work
    print("To test admin endpoints:")
    print("1. Run: python create_admin.py")
    print("2. Create an admin user")
    print("3. Login with admin credentials")
    print("4. Use the admin token to test admin endpoints")

if __name__ == "__main__":
    login_and_test_protected()
    test_admin_login() 