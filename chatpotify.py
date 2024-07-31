import openai
import spotipy
from spotify_auth import sp
import config
import time

# Set up OpenAI API key
from openai import OpenAI, OpenAIError

client = OpenAI(
  api_key=config.OPENAI_API_KEY,
)

def search_playlists(theme):
    results = sp.search(q=theme, limit=10, type='playlist')
    playlists = results['playlists']['items']
    return [playlist['id'] for playlist in playlists]

def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks

def create_playlist(theme, user_id):
    playlist_name = f"{theme} Playlist"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    return playlist['id']

def add_tracks_to_playlist(playlist_id, tracks):
    batch_size = 100
    for i in range(0, len(tracks), batch_size):
        sp.playlist_add_items(playlist_id, [track['track']['id'] for track in tracks[i:i+batch_size]])

def display_tracks(tracks, start=0, count=10):
    end = start + count
    for i, track in enumerate(tracks[start:end], start=start + 1):
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        print(f"{i}. '{track_name}' by '{artist_name}'")

def generate_chatgpt_response(prompt):
    retries = 3
    for i in range(retries):
        try:
            response = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:  # Use the correct error class
            if isinstance(e, OpenAIError) and i < retries - 1:  # i is zero indexed
                print(f"Rate limit exceeded, retrying in {2 ** i} seconds...")
                time.sleep(2 ** i)
            else:
                print(f"An error occurred: {str(e)}")
                raise

def chat():
    print("Chatpotify: Hello! I can help you create theme-based playlists on Spotify. What theme would you like?")
    user_id = sp.current_user()['id']  # Get the authenticated user's Spotify ID

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatpotify: Goodbye!")
            break

        theme = user_input
        prompt = f"The user wants to create a playlist with the theme '{theme}'. What are some popular songs and artists that fit this theme?"
        try:
            chatgpt_response = generate_chatgpt_response(prompt)
            print(f"Chatpotify: {chatgpt_response}")
        except OpenAIError as e:
            if isinstance(e, OpenAIError):
                print("Unable to generate a response from OpenAI due to rate limit. Please try again later.")
            else:
                print(f"An error occurred: {str(e)}")
            continue

        playlist_id = create_playlist(theme, user_id)
        print(f"Chatpotify: Created a playlist named '{theme} Playlist'. Adding some tracks...")

        # Search for playlists based on the theme
        playlist_ids = search_playlists(theme)
        
        if not playlist_ids:
            print(f"Chatpotify: No playlists found for the theme '{theme}'.")
            continue

        # Collect tracks from the found playlists, limiting to 200 tracks
        tracks = []
        for pid in playlist_ids:
            tracks.extend(get_playlist_tracks(pid))
            if len(tracks) >= 200:
                tracks = tracks[:200]
                break

        # Add the collected track IDs to the playlist
        add_tracks_to_playlist(playlist_id, tracks)
        print(f"Chatpotify: Added {len(tracks)} tracks to the playlist '{theme} Playlist'.")

        # Ask the user if they want to see the tracks
        while True:
            user_input = input("Do you want to see which tracks are included? (y/n): ").lower()
            if user_input in ['y', 'yes']:
                # Display the tracks with pagination
                start = 0
                while start < len(tracks):
                    display_tracks(tracks, start=start, count=10)
                    start += 10
                    if start < len(tracks):
                        user_input = input("Type 'next' to see more tracks or 'close' to exit: ").lower()
                        if user_input == 'close':
                            break
                break
            elif user_input in ['n', 'no']:
                break
            else:
                print("Invalid input. Please type 'y' for yes or 'n' for no.")

if __name__ == "__main__":
    chat()
