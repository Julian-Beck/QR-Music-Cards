import requests
import re

def get_reddit_post_comments(post_url):
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

        return comments_to_return

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}")  # Handle other errors

def extract_track_ids(urls):
    pattern = r'(?<=/track/)[a-zA-Z0-9]{22}'
    matches = re.findall(pattern, urls) 
    return matches

def save_data(data, project_name):
    with open(f"./csv/{project_name}-urls.csv", "w") as file:
        for url in data:
            file.write(f"https://open.spotify.com/track/{url}\n")

def comments_to_url(project_name, post_url):
    comments = get_reddit_post_comments(post_url)

    data = []
    for comment in comments:
        ids = extract_track_ids(comment)
        for id in ids:
            if not id in data:
                data.append(id)
    
    save_data(data, project_name)

if __name__ == "__main__":
    url = "https://www.reddit.com/r/hardstyle/comments/h81j4g/" # "<insert url of reddit post (like https://www.reddit.com/r/hardstyle/comments/ID)>"
    comments_to_url(url)