import os 
from dotenv import load_dotenv
import requests
import base64

from langchain.agents.tools import tool

load_dotenv()
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
SPOTIFY_ID = os.getenv("SPOTIFY_ID")

auth_str = f"{SPOTIFY_ID}:{SPOTIFY_SECRET}"

class SpotifyTools:

    def __init__(self):
        self.b64_auth = base64.b64encode(auth_str.encode()).decode()

        self.headers = {
                "Authorization": f"Basic {self.b64_auth}",
                "Content-Type": "application/x-www-form-urlencoded",
            }

    # @tool
    def get_access_token(self):

        data = {"grant_type": "client_credentials"}

        res = requests.post("https://accounts.spotify.com/api/token", headers=self.headers, data=data)
        access_token = res.json()["access_token"]
        return access_token

    # @tool
    def search_item(self):
        search_url = "https://api.spotify.com/v1/search"
        params = {
            "q": "The Daily", 
            "type": "show",
            "limit": 1
        }
        headers = {"Authorization": f"Bearer {self.get_access_token()}"}

        res = requests.get(search_url, headers=headers, params=params)

        return res

    # @tool
    def get_show_id(self):
        show = self.search_item().json()["shows"]["items"][0]
        show_id = show["id"]

        return show_id

    @staticmethod
    @tool(description="fecth episodes of a podcast from spotify in real time")
    def get_episodes():

        episodes_url = f"https://api.spotify.com/v1/shows/{SpotifyTools().get_show_id()}/episodes"
        # print(type(episodes_url))
        headers = {"Authorization": f"Bearer {SpotifyTools().get_access_token()}"}
        params = {"limit": 5}  # Adjust to how many episodes you want
        
        res = requests.get(episodes_url, headers=headers, params=params)
        episodes = res.json()["items"]

        result = ""
        for ep in episodes:
            print(f"Title: {ep['name']}")
            print(f"Episode ID: {ep['id']}")
            print(f"Episode URL: {ep['external_urls']['spotify']}\n")
            result += f"Title: {ep['name']}\n Episode ID: {ep['id']}\n Episode URL: {ep['external_urls']['spotify']}"
        return result