import requests
import json
import socket

baseurl = "http://localhost:8000"
url = "https://fndc-backend.onrender.com"

# Test basic connectivity to local server
def test_connectivity():
    try:
        print("Testing basic connectivity to local server...")
        # Try to connect to the local host
        host = "localhost"
        port = 8000
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Can reach {host}:{port}")
            return True
        else:
            print(f"❌ Cannot reach {host}:{port} - Is the server running?")
            return False
    except Exception as e:
        print(f"❌ Connectivity test failed: {e}")
        return False

# Test health check first
def test_health():
    try:
        print("Testing health endpoint...")
        response = requests.get(f"{baseurl}/health", timeout=5)
        print(f"Health Check - Status Code: {response.status_code}")
        print(f"Health Check - Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("❌ Health check timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Health check failed - server not running")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

# Test root endpoint
def test_root():
    try:
        print("\nTesting root endpoint...")
        response = requests.get(f"{baseurl}/", timeout=5)
        print(f"Root - Status Code: {response.status_code}")
        print(f"Root - Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("❌ Root endpoint timed out")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Root endpoint failed - server not running")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

# Test getting all tournaments (public endpoint)
def test_get_tournaments():
    try:
        print("\nTesting tournaments endpoint...")
        response = requests.get(f"{baseurl}/tournaments/", timeout=5)
        
        print(f"Tournaments - Status Code: {response.status_code}")
        print(f"Tournaments - Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            tournaments = response.json()
            print(f"✅ Success! Found {len(tournaments)} tournaments:")
            for tournament in tournaments:
                print(f"  - {tournament.get('name', 'N/A')} (ID: {tournament.get('id', 'N/A')})")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Tournaments endpoint timed out")
    except requests.exceptions.ConnectionError:
        print("❌ Tournaments endpoint failed - server not running")
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        print(f"Raw response: {response.text}")

if __name__ == "__main__":
    print("Testing API endpoints on LOCALHOST...")
    print("=" * 50)
    
    # Test connectivity first
    if test_connectivity():
        print("\n✅ Local server is reachable, testing endpoints...")
        
        # Test health first
        health_ok = test_health()
        
        # Test root
        root_ok = test_root()
        
        # Only test tournaments if basic endpoints work
        if health_ok and root_ok:
            print("\n✅ Basic endpoints working, testing tournaments...")
            test_get_tournaments()
        else:
            print("\n❌ Basic endpoints not working, skipping tournaments test")
    else:
        print("\n❌ Local server is not reachable - start the server with: python run.py") 