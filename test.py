import requests

baseurl = "http://0.0.0.0:8000"
url = "https://fndc-backend.onrender.com"

# Test getting all tournaments (public endpoint)
def test_get_tournaments():
    try:
        # Use the public tournaments endpoint
        response = requests.get(f"{url}/tournaments/")
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            tournaments = response.json()
            print(f"✅ Success! Found {len(tournaments)} tournaments:")
            for tournament in tournaments:
                print(f"  - {tournament.get('name', 'N/A')} (ID: {tournament.get('id', 'N/A')})")
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    print("Testing public tournaments endpoint...")
    test_get_tournaments() 