import requests
import re
import json

url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
}

response = requests.get(url, headers=headers)

try:
    # Directly parse the JSON response
    data = response.json()
    
    # Print number of events
    print(f"Total Games: {len(data.get('events', []))}")
    
    # Print details for each game
    for game in data.get('events', []):
        try:
            # Extract team and score information
            competitors = game['competitions'][0]['competitors']
            home_team = next(team for team in competitors if team['homeAway'] == 'home')
            away_team = next(team for team in competitors if team['homeAway'] == 'away')
            
            print(f"{away_team['team']['name']} ({away_team['score']}) @ {home_team['team']['name']} ({home_team['score']})")
        except Exception as e:
            print(f"Error parsing game: {e}")

except json.JSONDecodeError:
    print("Failed to decode JSON")
    print(response.text[:500])  # Print first 500 characters for debugging