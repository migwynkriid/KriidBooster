import os
import time
import steam
from steam.client import SteamClient
from steam.enums import EResult
from dotenv import load_dotenv

class SteamBooster:
    def __init__(self):
        self.client = SteamClient()
        self.logged_in = False
        load_dotenv()

    def login(self):
        """Login to Steam using credentials from environment variables"""
        username = os.getenv('STEAM_USERNAME')
        password = os.getenv('STEAM_PASSWORD')

        if not username or not password:
            print("Error: Steam credentials not found in environment variables")
            return False

        try:
            result = self.client.cli_login(username=username, password=password)
            if result == EResult.OK:
                self.logged_in = True
                print(f"Successfully logged in as {username}")
                return True
            else:
                print(f"Failed to log in: {result}")
                return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def get_owned_games(self):
        """Get list of owned games"""
        if not self.logged_in:
            print("Not logged in")
            return []

        try:
            games = self.client.get_owned_games()
            return games
        except Exception as e:
            print(f"Error getting owned games: {e}")
            return []

    def start_boosting(self, app_id):
        """Start boosting hours for a specific game"""
        if not self.logged_in:
            print("Not logged in")
            return False

        try:
            self.client.games_played([app_id])
            print(f"Started boosting game with ID: {app_id}")
            return True
        except Exception as e:
            print(f"Error starting game boost: {e}")
            return False

    def stop_boosting(self):
        """Stop boosting any running games"""
        if not self.logged_in:
            return

        try:
            self.client.games_played([])
            print("Stopped boosting all games")
        except Exception as e:
            print(f"Error stopping game boost: {e}")

def main():
    booster = SteamBooster()
    
    # Login to Steam
    if not booster.login():
        return

    # Get list of owned games
    games = booster.get_owned_games()
    if not games:
        print("No games found or error occurred")
        return

    # Display available games
    print("\nAvailable games:")
    for i, game in enumerate(games, 1):
        print(f"{i}. {game.name} (ID: {game.app_id})")

    # Get user input for game selection
    try:
        choice = int(input("\nEnter the number of the game you want to boost (0 to exit): "))
        if choice == 0:
            return
        if 1 <= choice <= len(games):
            selected_game = games[choice - 1]
            print(f"\nStarting to boost {selected_game.name}...")
            if booster.start_boosting(selected_game.app_id):
                print("Press Ctrl+C to stop boosting")
                try:
                    while True:
                        time.sleep(1)
                except KeyboardInterrupt:
                    booster.stop_boosting()
                    print("\nBoosting stopped")
        else:
            print("Invalid selection")
    except ValueError:
        print("Invalid input")

if __name__ == '__main__':
    main()