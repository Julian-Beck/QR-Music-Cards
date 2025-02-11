from src.Comments_To_Url import comments_to_url
from src.Playlist_To_Url import playlist_to_url
from src.Urls_To_Data import urls_to_data, test_secrets
from src.Data_To_PDF import data_to_pdf

if __name__ == "__main__":
    test_secrets()

    project_name = input("Please enter a name for the Project: ")
    post_url = input("Please enter the link for the source (enter for default): ")
    if post_url == "": post_url = "https://open.spotify.com/playlist/54J4amTEwP9iHXLtGqv1Vj"

    if "spotify" in post_url:
        playlist_to_url(project_name, post_url)
    elif "reddit" in post_url:
        comments_to_url(project_name, post_url)

    urls_to_data(project_name)

    data_to_pdf(project_name)




    
