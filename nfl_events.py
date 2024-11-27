import requests

# Replace with your actual RapidAPI key
api_key = "1f47e2de1dmsh8eaa1831c669a1cp1eb627jsnc729c0cf4100"

# Endpoint to get NFL scores (check the API documentation for the correct endpoint)
url = "https://nfl-data.p.rapidapi.com/games"

# Set up the headers with the API key
headers = {
    "X-RapidAPI-Host": "nfl-data.p.rapidapi.com",
    "X-RapidAPI-Key": api_key
}

# Make the API request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    print(data)  # This will print the data, you can modify it to extract specific info
else:
    print(f"Failed to retrieve data: {response.status_code}")
