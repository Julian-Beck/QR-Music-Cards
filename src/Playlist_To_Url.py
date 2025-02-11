import requests
from src.Urls_To_Data import read_access_secrets

def get_ID_from_url(url):
    id = url.split('/')[-1]
    if '?' in id : return id.split('?')[0] 
    else: return id

def make_request(url_playlist, access, token_type):
    id = get_ID_from_url(url_playlist)
    url_request = f"https://api.spotify.com/v1/playlists/{id}"
    headers = {
        "Authorization": f"{token_type} {access}"
    }

    try:
        # Make a GET request to the Spotify API
        response = requests.get(url_request, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        return response.json()["tracks"]["items"]

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}") 

def save_data(data, project_name):
    with open(f"./csv/{project_name}-urls.csv", "w") as file:
        for url in data:
            file.write(f"https://open.spotify.com/track/{url}\n")

def playlist_to_url(project_name, playlist_url):
    access, token_type = read_access_secrets()

    tracks = make_request(playlist_url, access, token_type)
    data = [track["track"]["id"] for track in tracks if not track["track"]["is_local"]]
    save_data(data, project_name)
    
if __name__ == "__main__":
    name = "test"
    playlist_url = "https://open.spotify.com/playlist/54J4amTEwP9iHXLtGqv1Vj"
    playlist_to_url(name, playlist_url)