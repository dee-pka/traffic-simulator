import requests
import json

# Replace with your Google Maps API key
API_KEY = 'YOUR_GOOGLE_MAPS_API_KEY'

def fetch_traffic_data(start_point, end_point):
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': start_point,
        'destination': end_point,
        'key': API_KEY,
        'traffic_model': 'best_guess',
        'departure_time': 'now'
    }
    response = requests.get(url, params=params)
    return response.json()

def parse_traffic_data(data):
    routes = data.get('routes', [])
    if not routes:
        return None
    
    route = routes[0]
    legs = route.get('legs', [])[0]
    
    distance = legs.get('distance', {}).get('text', 'N/A')
    duration = legs.get('duration', {}).get('text', 'N/A')
    duration_in_traffic = legs.get('duration_in_traffic', {}).get('text', 'N/A')
    
    steps = legs.get('steps', [])
    instructions = [step.get('html_instructions', '') for step in steps]
    
    return {
        'distance': distance,
        'duration': duration,
        'duration_in_traffic': duration_in_traffic,
        'instructions': instructions
    }

def display_traffic_info(info):
    if not info:
        print("No route found.")
        return
    
    print(f"Distance: {info['distance']}")
    print(f"Estimated Duration: {info['duration']}")
    print(f"Estimated Duration in Traffic: {info['duration_in_traffic']}")
    print("Directions:")
    for i, instruction in enumerate(info['instructions']):
        print(f"{i + 1}. {instruction}")

def main():
    start_point = input("Enter the starting point: ")
    end_point = input("Enter the destination: ")
    
    print("Fetching traffic data...")
    data = fetch_traffic_data(start_point, end_point)
    traffic_info = parse_traffic_data(data)
    display_traffic_info(traffic_info)

if __name__ == "__main__":
    main()
