import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials


def connect_spotify(client_id: str, client_secret: str):
    """
    This function is used to connect to the Spotify API
    :return: Spotify connection object
    """
    try:
        spot = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )
        return spot
    except Exception as e:
        print(f"[ Error | In connect_spotify function: {e}]")
        return None


def get_artist_for_name(client_id: str, client_secret: str, name: str, qnt_albums: int):
    """This function is used to get the artist for a given name

    Args:
        name (string): name of the artist

    Returns:
        list: list of artists
    """
    try:
        spot = connect_spotify(client_id, client_secret)
        result = spot.search(name)
        items = result["tracks"]["items"]
        if len(items) > 0:
            artist = items[0]["artists"][0]
            albums = get_albuns_of_artist(name, artist["id"], spot, qnt_albums)
            return albums
        else:
            return None
    except Exception as e:
        print(f"[ Error | In get_artist_for_name function: {e}]")
        return None


def get_albuns_of_artist(
    artist_name: str, artist_id: str, spot_connection: str, qnt_albums: int
):
    """This function is used to get the data of an artist for a given artist id

    Args:
        artist_id (string): artist id

    Returns:
        dict: album data
    """
    try:
        albuns = {}
        artist_data = spot_connection.artist_albums(artist_id, limit=qnt_albums)
        for i in range(len(artist_data["items"])):
            id = artist_data["items"][i]["id"]
            name = artist_data["items"][i]["name"]
            date_release = artist_data["items"][i]["release_date"]
            total_tracks = artist_data["items"][i]["total_tracks"]
            albuns[f"{artist_name.replace(' ','_')}_{i}"] = {
                "album_id": id,
                "album_name": name,
                "date_release": date_release,
                "total_tracks": total_tracks,
                "artist_name": artist_name,
            }
        return albuns
    except Exception as e:
        print(f"[ Error | In get_data_of_artist function: {e}]")
        return None
