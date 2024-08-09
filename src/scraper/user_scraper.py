import requests
import os
from dotenv import load_dotenv
from src.schemas.user_schema import user_schema, searched_user_schema
from src.scraper.post_scraper import instagramUserPostScraper
from src.utils.csv_creator import csvCreator


load_dotenv()

###############

instagramApiUrl = os.getenv("INSTAGRAM_API_URL")
instagramApiKey = os.getenv("INSTAGRAM_API_KEY")
instagramApiHost = os.getenv("INSTAGRAM_API_HOST")

###############

youtubeApiUrl = os.getenv("YOUTUBE_API_URL")
youtubeApiKey = os.getenv("YOUTUBE_API_KEY")
youtubeApiHost = os.getenv("YOUTUBE_API_HOST")
youtubeKey = os.getenv("YOUTUBE_KEY")

##############


def instagramUserScraper(user):
    headers = {
        "x-rapidapi-key": instagramApiKey,
        "x-rapidapi-host": instagramApiHost,
    }

    querystring = {"username_or_id_or_url": user}

    response = requests.get(
        instagramApiUrl + "/v1/similar_accounts", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()

        # print(data["data"]["items"])

        if "items" in data['data']:
            # userData = data["data"]["items"]

            # userDict = {
            #     "user_id": userData.get("id"),
            #     "full_name": userData.get("full_name"),
            #     "postCount": userData.get("media_count"),
            #     "follower_count": userData.get("follower_count"),
            # }
            # csvCreator([userDict], userSchema, "./csv/instagram/user.csv")

            # extracted_data = []

            users = data["data"]["items"]

            for id in range(3):
                instagramUserPostScraper(users[id].get("id"))
                instagramUserDataScraper(users[id].get("id"))
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")


def instagramUserDataScraper(user):

    headers = {
        "x-rapidapi-key": instagramApiKey,
        "x-rapidapi-host": instagramApiHost,
    }

    querystring = {"username_or_id_or_url": user, "include_about": "true"}

    response = requests.get(
        instagramApiUrl + "/v1/info", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()

        if "data" in data:

            # print(data)
            userData = data["data"]

            if userData["about"]["country"] == "India" and (
                userData["follower_count"] >= 5000 and userData["follower_count"] <= 100000
            ):
                modify_user_data = {
                    "user_id": userData.get("id"),
                    "username": userData.get("username"),
                    "full_name": userData.get("full_name"),
                    "post_count": userData.get("media_count"),
                    "post_frequency": None,
                    "follower_count": userData.get("follower_count"),
                }

                csvCreator([modify_user_data],user_schema,"./csv/instagram/user.csv",)
                # return modify_user_data
            else:
                print("User is not Indian")

        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")


def youtubeUserDataScraper(user):
    headers = {
        "x-rapidapi-key": youtubeApiKey,
        "x-rapidapi-host": youtubeApiHost,
    }

    querystring = {
        "part": "snippet,id",
        "key": youtubeKey,
        "channelType": "any",
        "maxResults": "50",
        "q": "motorbloging",
        "regionCode": "In",
        "type": "channel",
    }

    response = requests.get(
        youtubeApiUrl + "/search", headers=headers, params=querystring
    )

    data = response.json()

    if response.status_code == 200:
        data = response.json()

        if "items" in data:
            extracted_data = []

            for item in data["items"]:
                extracted_data.append(
                    {
                        "user_id": item.get("snippet").get("channelId"),
                        "full_name": item.get("snippet").get("channelTitle"),
                        "postCount": item.get("snippet").get("channelTitle"),
                        "follower_count": item.get("snippet").get("subscriber"),
                    }
                )
            csvCreator(extracted_data, userSchema, "./csv/youtube/user.csv")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")
