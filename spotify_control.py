import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API Credentials
SPOTIFY_CLIENT_ID = "0acd5367cd0a464dbe3a84ecadf2d195"
SPOTIFY_CLIENT_SECRET = "5f87c2d5444545cea8a4d28f70be0d46"
SPOTIFY_REDIRECT_URI = "http://localhost:8080"

# Initialize Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state user-library-modify user-read-currently-playing"
))

def get_active_device():
    devices = sp.devices()
    if devices['devices']:
        return devices['devices'][0]['id']
    return None

# Function to play/pause music
def play_pause_music():
    playback = sp.current_playback()
    if playback and playback['is_playing']:
        sp.pause_playback()
    else:
        sp.start_playback()

# Function to play next or previous song
def skip_song():
    sp.next_track()

def previous_song():
    sp.previous_track()

# Function to like the currently playing song
def like_song():
    track = sp.current_playback()
    if track:
        song_id = track['item']['id']
        sp.current_user_saved_tracks_add([song_id])

# Function to play a specific album or artist
def play_album_by_artist(artist_name):
    results = sp.search(q=f"album:{artist_name}", type="album", limit=1)
    if results['albums']['items']:
        album_uri = results['albums']['items'][0]['uri']
        sp.start_playback(context_uri=album_uri)

# Function to play an artist's songs
def play_artist(artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    if results['artists']['items']:
        artist_uri = results['artists']['items'][0]['uri']
        sp.start_playback(context_uri=artist_uri)

# Function to control volume
def set_volume(level):
    sp.volume(level)

# Main function to handle commands
def handle_spotify_command(command):
    if "play music" in command:
        play_pause_music()
    elif "pause" in command:
        play_pause_music()
    elif "next song" in command:
        skip_song()
    elif "previous song" in command:
        previous_song()
    elif "like this song" in command:
        like_song()
    elif "play album by" in command:
        artist = command.replace("play album by", "").strip()
        play_album_by_artist(artist)
    elif "play artist" in command:
        artist = command.replace("play artist", "").strip()
        play_artist(artist)
    elif "increase volume" in command:
        set_volume(80)  # Set volume to 80%
    elif "decrease volume" in command:
        set_volume(30)  # Set volume to 30%
