# chatpotify.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_auth import sp
import config

def search_playlists(theme):
    """
    Searches for Spotify playlists based on the given theme.

    Parameters:
    theme (str): The theme to search for playlists.

    Returns:
    list: A list of playlist IDs matching the theme.
    """
    results = sp.search(q=theme, limit=10, type='playlist')
    playlists = results['playlists']['items']
    return [playlist['id'] for playlist in playlists]

def get_playlist_tracks(playlist_id):
    """
    Retrieves all track IDs from a given playlist.

    Parameters:
    playlist_id (str): The ID of the Spotify playlist.

    Returns:
    list: A list of track objects from the playlist.
    """
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    return tracks

def create_playlist(theme, user_id):
    """
    Creates a new playlist on Spotify with the given theme.

    Parameters:
    theme (str): The theme for the playlist.
    user_id (str): The Spotify user ID.

    Returns:
    str: The ID of the created playlist.
    """
    playlist_name = f"{theme} Playlist"
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=True)
    return playlist['id']

def add_tracks_to_playlist(playlist_id, tracks):
    """
    Adds tracks to the specified Spotify playlist in batches.

    Parameters:
    playlist_id (str): The ID of the Spotify playlist.
    tracks (list): A list of Spotify track objects to add to the playlist.
    """
    batch_size = 100
    for i in range(0, len(tracks), batch_size):
        sp.playlist_add_items(playlist_id, [track['track']['id'] for track in tracks[i:i+batch_size]])

def display_tracks(tracks, start=0, count=10):
    """
    Displays the song names and artists in the format "songname" by "artist", with pagination.

    Parameters:
    tracks (list): A list of track objects.
    start (int): The starting index of tracks to display.
    count (int): The number of tracks to display.
    """
    end = start + count
    for i, track in enumerate(tracks[start:end], start=start + 1):
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']
        print(f"{i}. '{track_name}' by '{artist_name}'")

def chat():
    """
    Main function to handle the chat interaction with the user.
    """
    print("Chatpotify: Hello! I can help you create theme-based playlists on Spotify after the name of your playlist. For example: 'Summer vibes'. What theme would you like?")
    user_id = sp.me()['id']  # Get the authenticated user's Spotify ID

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatpotify: Goodbye!")
            break

        theme = user_input
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
