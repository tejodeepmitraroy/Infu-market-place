import requests
import os
from dotenv import load_dotenv
from src.schemas.user_schema import user_schema, searched_user_schema
from src.scraper.post_scraper import instagramUserPostScraper, youtubeUserVideosScraper
from src.utils.csv_creator import csvCreator
from src.utils.difference_between_csv import difference_between_csv
from src.utils.difference_between_list import difference_between_list
from src.utils.csv_to_list import csv_to_list


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

        if "items" in data["data"]:
            users = data["data"]["items"]

            extracted_data = []

            for item in users:

                extracted_data.append(
                    {
                        "user_id": item.get("id"),
                        "username": item.get("username"),
                    }
                )

            csvCreator(
                extracted_data,
                searched_user_schema,
                "./csv/instagram/searched_users.csv",
            )

            # if os.path.exists("./csv/instagram/user.csv"):
            if os.path.exists("./csv/instagram/rejected_user.csv"):
                non_rejected_users = difference_between_csv(
                    "./csv/instagram/searched_users.csv",
                    "./csv/instagram/rejected_user.csv",
                    "user_id",
                    "user_id",
                )

                user_ids = csv_to_list("./csv/instagram/user.csv", "user_id")

                if user_ids:
                    unique_users = difference_between_list(non_rejected_users, user_ids)
                else:
                    unique_users = non_rejected_users
            else:
                searched_user_ids = csv_to_list(
                    "./csv/instagram/searched_users.csv", "user_id"
                )

                unique_users = searched_user_ids

            # print(non_rejected_users)
            # print(unique_users)

            # for id in unique_users:
            #     instagramUserDataScraper(unique_users[id])

            for user_id in unique_users:
                instagramUserDataScraper(user_id)


            if os.path.exists("./csv/instagram/post.csv"):
                filtered_users_ids = non_existed_users = difference_between_csv(
                    "./csv/instagram/user.csv",
                    "./csv/instagram/post.csv",
                    "user_id",
                    "user_id",
                )
            else:
                filtered_users_ids = csv_to_list("./csv/instagram/user.csv", "user_id")


            print("This is not existed users in Post DB ====> /n",non_existed_users)

            if filtered_users_ids:
                print("Initiating Instagram Post Scrapping")
                for user_id in filtered_users_ids:
                    instagramUserPostScraper(user_id)

            print("Instagram Data Scraped")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code", response.status_code)


def instagramUserDataScraper(user_id: str):

    headers = {
        "x-rapidapi-key": instagramApiKey,
        "x-rapidapi-host": instagramApiHost,
    }

    querystring = {"username_or_id_or_url": user_id, "include_about": "true"}

    response = requests.get(
        instagramApiUrl + "/v1/info", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()

        if "data" in data:
            userData = data["data"]

            print(userData.get("follower_count"))

            if (
                userData["about"]["country"] == "India"
                and userData.get("follower_count")
                and (
                    userData.get("follower_count") >= 5000
                    and userData.get("follower_count") <= 100000
                )
            ):

                modify_user_data = {
                    "user_id": userData.get("id"),
                    "username": userData.get("username"),
                    "category": userData.get("category"),
                    "full_name": userData.get("full_name"),
                    "post_count": userData.get("media_count"),
                    "post_frequency": (
                        userData.get("media_count") / 5
                        if userData.get("media_count")
                        else None
                    ),
                    "follower_count": userData.get("follower_count"),
                }

                csvCreator(
                    [modify_user_data],
                    user_schema,
                    "./csv/instagram/user.csv",
                )
            else:
                modify_user_data = {
                    "user_id": userData.get("id"),
                    "username": userData.get("username"),
                    "category": userData.get("category"),
                    "full_name": userData.get("full_name"),
                    "post_count": userData.get("media_count"),
                    "post_frequency": (
                        userData.get("media_count") / 5
                        if userData.get("media_count")
                        else None
                    ),
                    "follower_count": userData.get("follower_count"),
                }

                csvCreator(
                    [modify_user_data],
                    user_schema,
                    "./csv/instagram/rejected_user.csv",
                )

                print("User is not Indian Or Follower Count range is not satisfied")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code", response.status_code)


def youtubeChannelsScraper(search: str):
    headers = {
        "x-rapidapi-key": youtubeApiKey,
        "x-rapidapi-host": youtubeApiHost,
    }

    # querystring = {
    #     "part": "snippet,id",
    #     "key": youtubeKey,
    #     "maxResults": "50",
    #     "q": search,
    #     "regionCode": "In",
    #     "relevanceLanguage": "hi",
    #     "type": "channel",
    # }

    # Delhi based Users
    querystring = {
        "part": "snippet,id",
        "key": youtubeKey,
        "location": "28.664470662634336, 77.10763707905652",
        "locationRadius": "1000km",
        "maxResults": "50",
        "q": search,
        "regionCode": "In",
        "relevanceLanguage": "hi",
        "type": "video",
    }

    # # Kolkata based Users
    # querystring = {
    #     "part": "snippet",
    #     "key": youtubeKey,
    #     "location": "22.525258565355376, 88.34975242640142",
    #     "locationRadius": "1000km",
    #     "maxResults": "50",
    #     "q": search,
    #     "regionCode": "In",
    #     "relevanceLanguage": "hi",
    #     "type": "video",
    # }

    response = requests.get(
        youtubeApiUrl + "/search", headers=headers, params=querystring
    )

    data = response.json()

    if response.status_code == 200:
        data = response.json()

        if "items" in data:
            extracted_searched_channels = []

            for item in data["items"]:

                extracted_searched_channels.append(
                    {
                        "user_id": item.get("snippet").get("channelId"),
                        "username": item.get("snippet").get("channelTitle"),
                    }
                )

            csvCreator(
                extracted_searched_channels,
                searched_user_schema,
                "./csv/youtube/searched_users.csv",
            )

            searched_user_ids = csv_to_list(
                "./csv/youtube/searched_users.csv", "user_id"
            )

            # print("Youtube Searched Id---------->/n", searched_user_ids)

            # for id in range(2):
            #     youtubeUserDataScraper(searched_user_ids[id])

            for user_id in searched_user_ids:
                youtubeUserDataScraper(user_id)

            filtered_users_ids = csv_to_list("./csv/youtube/user.csv", "user_id")

            if filtered_users_ids:
                for user_id in filtered_users_ids:
                    youtubeUserVideosScraper(user_id)

            print("Youtube Data Scraped")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")


def youtubeUserDataScraper(user_id):
    headers = {
        "x-rapidapi-key": youtubeApiKey,
        "x-rapidapi-host": youtubeApiHost,
    }

    querystring = {
        "part": "brandingSettings,contentDetails, contentOwnerDetails, id, localizations, snippet, statistics, status, topicDetails",
        "key": "AIzaS9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6a7b8c9dTr",
        "id": user_id,
    }

    response = requests.get(
        youtubeApiUrl + "/channels", headers=headers, params=querystring
    )

    data = response.json()

    if response.status_code == 200:
        data = response.json()

        userData = data["items"][0]

        print(userData["statistics"]["subscriberCount"])

        if userData:

            if "country" in userData["snippet"]:
                if userData["snippet"]["country"] == "IN" and (
                    int(userData["statistics"]["subscriberCount"]) >= 5000
                    and int(userData["statistics"]["subscriberCount"]) <= 100000
                ):
                    # if int(userData["statistics"]["subscriberCount"]) >= 5000 and int(userData["statistics"]["subscriberCount"]) <= 100000:

                    modify_user_data = {
                        "user_id": userData["id"],
                        "username": userData["snippet"]["customUrl"],
                        "full_name": userData["snippet"]["title"],
                        "post_count": int(userData["statistics"]["videoCount"]),
                        "post_frequency": int(userData["statistics"]["videoCount"]) / 5,
                        "follower_count": int(
                            userData["statistics"]["subscriberCount"]
                        ),
                    }
                    csvCreator(
                        [modify_user_data], user_schema, "./csv/youtube/user.csv"
                    )
                    print("Channel is Added in list")
                    # return modify_user_data
                else:
                    print("not Between Follower Count")
            else:
                print("Another country value is existed")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")
