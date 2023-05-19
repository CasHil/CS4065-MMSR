import spacy
import spacy.cli
from textblob import TextBlob
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
spacy.cli.download("en_core_web_sm")
nlp = spacy.load('en_core_web_sm')
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                      client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(
    client_credentials_manager=client_credentials_manager)


def get_audio_features(track_uri):
    track_info = spotify.track(track_uri)
    audio_features = spotify.audio_features(track_uri)
    return track_info, audio_features[0]


def map_text_to_audio_features(text):
    doc = nlp(text)
    keywords = [
        token.lemma_ for token in doc if not token.is_stop and token.pos_ == 'NOUN']
    sentiment = TextBlob(text).sentiment.polarity
    query = ' '.join(keywords)
    search_results = spotify.search(q=query, type='track', limit=1)

    if search_results['tracks']['items']:
        track_uri = search_results['tracks']['items'][0]['uri']
        track_info, _ = get_audio_features(track_uri)
        valence = sentiment
        energy = sentiment if sentiment >= 0 else 0
        loudness = sentiment * 10
        speechiness = len(keywords) / len(doc)
        acousticness = 1 - speechiness
        instrumentalness = sentiment if sentiment < 0 else 0
        liveness = 1 - sentiment if sentiment >= 0 else 0

        valence = max(0, min(1, valence))
        energy = max(0, min(1, energy))
        speechiness = max(0, min(1, speechiness))
        acousticness = max(0, min(1, acousticness))
        instrumentalness = max(0, min(1, instrumentalness))
        liveness = max(0, min(1, liveness))
        loudness = max(-60, min(0, loudness))
        return {
            'track_info': track_info,
            'audio_features': {
                'energy': energy,
                'loudness': loudness,
                'speechiness': speechiness,
                'acousticness': acousticness,
                'instrumentalness': instrumentalness,
                'liveness': liveness,
                'valence': valence
            }
        }
    else:
        return None


text = "The best song ever made by the best band ever."
result = map_text_to_audio_features(text)
if result:
    print("Track Name:", result['track_info']['name'])
    print("Artist:", result['track_info']['artists'][0]['name'])
    print("Mapped Audio Features:")
    for feature, value in result['audio_features'].items():
        print(f"{feature.capitalize()}: {value}")
else:
    print("No matching track found.")
