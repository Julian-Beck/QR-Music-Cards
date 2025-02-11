import requests
import configparser
import subprocess
import json

def read_request_data():
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
        artists = get_artist_string(json_response["artists"])
        track = json_response["name"]
        year = json_response["album"]["release_date"][:4]
        return artists, track, year, url_song

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}") 

def get_reddit_post_comments(post_url):
    try:
        command = f"curl -s {post_url}.json"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("Error fetching data:", result.stderr)
            return
        
        data = json.loads(result.stdout)
        comments_data = data[1]['data']['children']
        
        comments_to_return = []
        for comment in comments_data:
            if 'body' in comment['data']:
                comments_to_return.append(comment['data']['body'])
                print(f"{comment['data']['body']}\n")

        return comments_to_return
    
    except Exception as e:
        print("An error occurred:", e)

def get_reddit_post_comments_advanced(post_url):
    try:
        # Append '.json' to the post URL to get the comments in JSON format
        json_url = f"{post_url}.json"
        
        # Make a GET request to the Reddit API
        response = requests.get(json_url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse the JSON response
        data = response.json()
        comments_data = data[1]['data']['children']
        
        comments_to_return = []
        for comment in comments_data:
            if 'body' in comment['data']:
                comments_to_return.append(comment['data']['body'])
                print(f"{comment['data']['body']}\n")

        return comments_to_return

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}")  # Handle other errors

def save_data(data):
    with open("data.csv", "w") as file:
        for (artists, track, year, spotify_id) in data:
            file.write(f"{artists}, {track}, {year}, {spotify_id.split('?')[0]}\n")

if __name__ == "__main__":
    post_url = "<insert url of reddit post (like https://www.reddit.com/r/hardstyle/comments/ID)>"

    comments = get_reddit_post_comments(post_url)
    comments = ['https://open.spotify.com/track/12FwJBQbg71k7EMPz7aHlj',
                'https://open.spotify.com/track/5DaHRGpgfmx7mcCYrXmlxT',
                'https://open.spotify.com/track/4IQRBdStUUgT2dExFKQYsN',
                'https://open.spotify.com/track/5DYMuWtQyr1J9Af0SMrDz8']

    access, token_type = read_request_data()
    data_list = [make_request(comment, access, token_type) for comment in comments]
    save_data(data_list)
