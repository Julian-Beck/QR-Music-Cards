import subprocess
import json

def extract_info(comment: str):
    first = comment.find("-")
    second = comment.find("[")
    third = comment.find("]")

    if first != -1 and second != -1 and third != -1: 
        artist = comment[:first].strip()  # Extract artist
        track = comment[first+1:second].strip()  # Extract track
        year = comment[second+1:third].strip()
        spotify_id = comment[third+1:].strip()
        
        return artist, track, year, spotify_id
    else:
        print("The comment format is incorrect.")
        return None, None, None, None
    

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

def save_data(data):
    with open("data.csv", "w") as file:
        for (artist, track, year, spotify_id) in data:
            file.write(f"{artist}, {track}, {year}, {spotify_id.split('?')[0]}\n")

if __name__ == "__main__":
    post_url = "<insert url of reddit post (like https://www.reddit.com/r/hardstyle/comments/ID)>"

    comments = get_reddit_post_comments(post_url)
    data_list = [extract_info(comment) for comment in comments]
    save_data(data_list)
