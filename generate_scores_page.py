import requests
import json
from datetime import datetime, timezone
import os

def fetch_nfl_scores():
    url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
    }
    response = requests.get(url, headers=headers)
    return response.json()

def generate_html_scores(data):
    # Get current timestamp
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>NFL Scores</title>
        <meta http-equiv="refresh" content="60">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 20px; 
                background-color: #f4f4f4;
            }
            .game-container {
                background-color: white;
                border-radius: 8px;
                margin-bottom: 10px;
                padding: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .game-status {
                font-weight: bold;
                color: #666;
                margin-bottom: 10px;
                display: block;
            }
            .team {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            .team-logo {
                width: 50px;
                height: 50px;
                margin-right: 10px;
            }
            .team-name {
                margin-right: 10px;
                flex-grow: 1;
            }
            .score {
                font-weight: bold;
                font-size: 1.2em;
            }
            .last-updated {
                text-align: center;
                color: #888;
                margin-top: 20px;
                font-size: 0.8em;
            }
        </style>
    </head>
    <body>
        <h1>NFL Scores</h1>
    """

    for game in data.get('events', []):
        try:
            # Game details
            game_status = game.get('status', {})
            status_type = game_status.get('type', {})
            
            # Determine game status
            if status_type.get('state') == 'final':
                game_status_text = 'FINAL'
            else:
                # Combine quarter and time
                detail = status_type.get('detail', 'Not Started')
                game_status_text = detail

            competitors = game['competitions'][0]['competitors']
            home_team = next(team for team in competitors if team['homeAway'] == 'home')
            away_team = next(team for team in competitors if team['homeAway'] == 'away')
            
            # Team logos (using ESPN's default logo if not available)
            home_logo = home_team.get('team', {}).get('logo', 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/default-team-logo-500.png')
            away_logo = away_team.get('team', {}).get('logo', 'https://a.espncdn.com/combiner/i?img=/i/teamlogos/default-team-logo-500.png')

            html += f"""
            <div class="game-container">
                <span class="game-status">{game_status_text}</span>
                <div class="team">
                    <img src="{away_logo}" alt="{away_team['team']['name']} logo" class="team-logo">
                    <span class="team-name">{away_team['team']['name']}</span>
                    <span class="score">{away_team.get('score', '0')}</span>
                </div>
                <div class="team">
                    <img src="{home_logo}" alt="{home_team['team']['name']} logo" class="team-logo">
                    <span class="team-name">{home_team['team']['name']}</span>
                    <span class="score">{home_team.get('score', '0')}</span>
                </div>
            </div>
            """
        except Exception as e:
            print(f"Error parsing game: {e}")

    # Add last updated timestamp
    html += f"""
        <div class="last-updated">
            Last Updated: {current_time}
        </div>
    </body>
    </html>
    """

    return html

def main():
    # Fetch scores
    data = fetch_nfl_scores()
    
    # Generate HTML
    html_content = generate_html_scores(data)
    
    # Write to file with explicit flushing and syncing
    with open('index.html', 'w') as f:
        f.write(html_content)
        f.flush()  # Flush internal buffer
    os.fsync(f.fileno())  # Ensure file is written to disk
    
    print(f"NFL Scores updated at {datetime.now()}")

if __name__ == "__main__":
    main()