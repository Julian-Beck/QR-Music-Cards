import configparser
import requests

def read_request_data(config):
    user = config["REQUEST"].get("CLIENT_ID")
    password = config["REQUEST"].get("CLIENT_SECRET")
    return user, password

def make_request(user, password):
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": user,
        "client_secret": password
    }

    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()  # Return the response as JSON
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Handle HTTP errors
    except Exception as err:
        print(f"An error occurred: {err}")  # Handle other errors

def save_access_token_to_secrets(config, token, type):
    config.set("ACCESS", "ACCESS_TOKEN", token)
    config.set("ACCESS", "TOKEN_TYPE", type)
    with open('secrets.ini', 'w') as configfile:
        config.write(configfile)

def update_token():
    secrets = configparser.ConfigParser()
    secrets.read('secrets.ini')
    user, password = read_request_data(secrets)

    response = make_request(user, password)
    print(response["access_token"])

    save_access_token_to_secrets(secrets, response["access_token"], response["token_type"])
    print("Generated new token!")
    
if __name__ == "__main__":
    update_token()