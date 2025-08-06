import requests
import json

baseurl = "http://localhost:8000"

def test_endpoint(name, method, path, data=None, headers=None):
    """Generic function to test any endpoint"""
    try:
        url = f"{baseurl}{path}"
        print(f"\n🔍 Testing {name}...")
        print(f"   {method} {url}")
        
        if method.upper() == "GET":
            response = requests.get(url, timeout=5, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=5, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, timeout=5, headers=headers)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ Success: {json.dumps(result, indent=2)}")
                return True
            except:
                print(f"   ✅ Success: {response.text}")
                return True
        else:
            print(f"   ❌ Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")
        return False

def test_public_endpoints():
    """Test all public endpoints (no authentication required)"""
    print("=" * 60)
    print("🌐 TESTING PUBLIC ENDPOINTS")
    print("=" * 60)
    
    # Basic endpoints
    test_endpoint("Health Check", "GET", "/health")
    test_endpoint("Root", "GET", "/")
    test_endpoint("API Info", "GET", "/docs")
    
    # Tournament endpoints (public)
    test_endpoint("List Tournaments", "GET", "/tournaments/")
    test_endpoint("Get Tournament by ID", "GET", "/tournaments/689173a65550a20c74c67494")
    
    # Cube endpoints (public)
    test_endpoint("Get Enabled Cubes", "GET", "/cubes/tournament/689173a65550a20c74c67494/enabled")

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n" + "=" * 60)
    print("🔐 TESTING AUTHENTICATION ENDPOINTS")
    print("=" * 60)
    
    # Test registration
    test_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123456"
    }
    test_endpoint("Register User", "POST", "/auth/register", test_data)
    
    # Test login
    login_data = {
        "username": "test@example.com",
        "password": "test123456"
    }
    test_endpoint("Login", "POST", "/auth/login", login_data)

def test_protected_endpoints(token):
    """Test protected endpoints (requires authentication)"""
    if not token:
        print("\n❌ No token provided, skipping protected endpoints")
        return
        
    print("\n" + "=" * 60)
    print("🔒 TESTING PROTECTED ENDPOINTS")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # User profile
    test_endpoint("Get User Profile", "GET", "/auth/me", headers=headers)
    test_endpoint("Get User Profile", "GET", "/users/profile", headers=headers)
    
    # Tournament registration
    test_endpoint("Register to Tournament", "POST", "/tournaments/689173a65550a20c74c67494/register", headers=headers)
    test_endpoint("Check My Registration", "GET", "/tournaments/689173a65550a20c74c67494/my-registration", headers=headers)
    
    # Cube proposal
    cube_data = {
        "tournament_id": "689173a65550a20c74c67494",
        "cube_url": "https://cubecobra.com/cube/list/test",
        "description": "Test cube proposal"
    }
    test_endpoint("Propose Cube", "POST", "/cubes/propose", cube_data, headers)

def test_admin_endpoints(admin_token):
    """Test admin endpoints (requires admin token)"""
    if not admin_token:
        print("\n❌ No admin token provided, skipping admin endpoints")
        return
        
    print("\n" + "=" * 60)
    print("👑 TESTING ADMIN ENDPOINTS")
    print("=" * 60)
    
    headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Admin endpoints
    test_endpoint("List All Users", "GET", "/users/", headers=headers)
    test_endpoint("Get All Cube Proposals", "GET", "/cubes/tournament/689173a65550a20c74c67494/all", headers=headers)
    
    # Create tournament
    tournament_data = {
        "name": "Test Tournament",
        "date": "2024-12-25T10:00:00Z",
        "location": "Test Location",
        "start_time": "10:00",
        "duration_days": 1,
        "rounds": 4
    }
    test_endpoint("Create Tournament", "POST", "/tournaments/", tournament_data, headers)

def main():
    print("🚀 FNDC API ENDPOINT TESTER")
    print("Testing local API at:", baseurl)
    
    # Test public endpoints
    test_public_endpoints()
    
    # Test auth endpoints
    test_auth_endpoints()
    
    # For protected endpoints, you would need to:
    # 1. Register/login to get a token
    # 2. Use that token in the Authorization header
    
    print("\n" + "=" * 60)
    print("📝 NOTES:")
    print("- Public endpoints work without authentication")
    print("- Protected endpoints require a valid JWT token")
    print("- Admin endpoints require an admin user token")
    print("- To test protected endpoints, login first and use the token")
    print("=" * 60)

if __name__ == "__main__":
    main() 