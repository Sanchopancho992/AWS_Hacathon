import requests
import json

# Test the itinerary endpoint
url = "http://127.0.0.1:8000/api/itinerary"
data = {
    "duration": 3,
    "interests": ["food", "culture"], 
    "budget": "medium",
    "travel_style": "moderate"
}

response = requests.post(url, json=data)
print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))
