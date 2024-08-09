# Chatpotify

Chatpotify is a chatbot that creates theme-based playlists on Spotify using OpenAI. Users can interact with the chatbot to specify a theme by giving the name of the playlist, and Chatpotify will create a playlist and optionally display the tracks included.

## Work in Progress

This project is currently a work in progress. Contributions and feedback are welcome!

## Features

- Creates playlists based on user-specified themes.
- Searches for existing Spotify playlists related to the theme.
- Adds tracks from these playlists to the new playlist, up to 200 tracks.
- Displays tracks in the playlist with pagination.

## Requirements

- Python 3.6+
- Spotify Developer Account
- OpenAI API Key

## Dependencies

Install the required dependencies using pip:

```
pip install spotipy python-dotenv
```

## Configuration

1. Spotify Developer Account:

- Create an application on the Spotify Developer [Dashboard](https://developer.spotify.com/dashboard/applications).
- Obtain your Client ID and Client Secret.
- Set a Redirect URI to http://localhost:8888/callback.

2. OpenAI Account:

Obtain your API key from the [OpenAI Dashboard](https://platform.openai.com/account/api-keys).

3. Environment Variables:

Create a .env file in the project directory and add your Spotify credentials:

```
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## Usage

1. Activate Virtual Environment:

If you are using a virtual environment, activate it:

```
source myenv/bin/activate
```

2. Run the Chatpotify Script:

```
python chatpotify.py
```

3. Interact with Chatpotify:

- Specify a theme for your playlist. Keep in mind that the theme will end up being the playlist's name. For example, entering:

```
Gothic mood
```

Will create a new plalist called "Gothic mood".

- Optionally, view the tracks added to the playlist with pagination. Enter yes (y) or no (n) to see which tracks are included.
- When the tracks are listed, type 'next' to see more tracks or 'close' to exit.

4. Exit Chatpotify:

Just type 'exit'.

```
exit
```

## Example

```
Chatpotify: Hello! I can help you create theme-based playlists on Spotify. What theme would you like?
You: Summer
Chatpotify: Created a playlist named 'Summer Playlist'. Adding some tracks...
Chatpotify: Added 200 tracks to the playlist 'Summer Playlist'.
Do you want to see which tracks are included? (y/n): y
1. 'Song1' by 'Artist1'
2. 'Song2' by 'Artist2'
Type 'next' to see more tracks or 'close' to exit: next
...
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details. Please take into account Spotify and OpenAI terms of use as well:

- By using this project, you agree to comply with the [Spotify Developer Terms of Service](https://developer.spotify.com/terms/). Make sure you review and understand these terms before using the Spotify API in your applications.

- By using this project, you agree to comply with the [OpenAI API Terms of Service](https://openai.com/policies/terms-of-use). Ensure you review and understand these terms before using the OpenAI API in your applications.