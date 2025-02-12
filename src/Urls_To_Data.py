import requests
import configparser
from tqdm import tqdm
from src.Update_Token import update_token

def test_secrets():
    access, token_type = read_access_secrets()
    headers = { "Authorization": f"{token_type} {access}" }
    try:
        # Make a GET request to the Spotify API
        test_url = "https://api.spotify.com/v1/tracks/6yAQLrV6OKum99rMFDWTZG"
        response = requests.get(test_url, headers=headers)
        response.raise_for_status()
    except Exception as err:
        print(f"An error occurred: {err}. Generate new access token!")
        update_token()

def read_access_secrets():
    config = configparser.ConfigParser()
    config.read('secrets.ini')
    access_token = config["ACCESS"].get("ACCESS_TOKEN")
    token_type = config["ACCESS"].get("TOKEN_TYPE")
    return access_token, token_type

def get_ID_from_url(url):
    id = url.split('/')[-1]
    if '?' in id : return id.split('?')[0] 
    else: return id

def get_artist_string(artists):
    ret = ""
    artists.reverse()
    for art in artists:
        name = art["name"]
        ret += f"{name}&&"
    return ret[:len(ret)-2]

def make_request(url_song, access, token_type):
    id = get_ID_from_url(url_song)
    url_request = f"https://api.spotify.com/v1/tracks/{id}"
    headers = {
        "Authorization": f"{token_type} {access}"
    }

    try:
        # Make a GET request to the Spotify API
        response = requests.get(url_request, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        
        json_response = response.json()
        artists = get_artist_string(json_response["artists"]).replace(",", ";")
        track = json_response["name"].replace(",", ";")
        year = json_response["album"]["release_date"][:4]
        return artists, track, year, url_song

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}") 

def read_data(project_name):
    data_list = []
    with open(f"./csv/{project_name}-urls.csv", "r") as file:
        for line in file:
            data_list.append(line.strip())
    return data_list

def save_data(data, project_name):
    with open(f"./csv/{project_name}-data.csv", "w") as file:
        for (artists, track, year, spotify_id) in data:
            file.write(f"{artists}, {track}, {year}, {spotify_id.split('?')[0]}\n")

def urls_to_data(project_name):
    comments = read_data(project_name)
    
    access, token_type = read_access_secrets()
    
    data_list=[]
    for comment in tqdm(comments):
        data_list.append(make_request(comment, access, token_type))

    data_list = [make_request(comment, access, token_type) for comment in comments]
    save_data(data_list, project_name)

if __name__ == "__main__":
    name = "test"
    urls_to_data(name)