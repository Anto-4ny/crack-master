import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# Function to scrape betting website
def scrape_betting_data(url):
    try:
        # Send a GET request to the webpage
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors

        # Parse the webpage content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract game data (replace 'div.class-name' with actual tags from the website)
        games = soup.find_all('div', class_='game-result')  # Example placeholder

        # Extract relevant data from each game
        results = []
        for game in games:
            multiplier = game.find('span', class_='multiplier').text  # Placeholder
            timestamp = game.find('span', class_='time').text  # Placeholder
            results.append({'Timestamp': timestamp, 'Multiplier': multiplier})

        return results

    except Exception as e:
        print(f"Error occurred: {e}")
        return []
# Function to save data to CSV
def save_to_csv(data, filename='betting_data.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
