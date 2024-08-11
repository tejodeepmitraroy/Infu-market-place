import requests
import os
from dotenv import load_dotenv
from src.schemas.post_schema import postSchema, searched_youtube_user_video_Schema
from src.utils.csv_creator import csvCreator
from src.utils.csv_to_list import csv_to_list
from src.utils.post_frequency_counter import post_frequency_counter


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


def instagramUserPostScraper(user_id: str):
    headers = {
        "x-rapidapi-key": instagramApiKey,
        "x-rapidapi-host": instagramApiHost,
    }

    querystring = {"username_or_id_or_url": user_id}

    response = requests.get(
        instagramApiUrl + "/v1.2/posts", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()

        if "data" in data:

            extracted_post_data = []

            for item in data["data"]["items"]:
                extracted_post_data.append(
                    {
                        "post_id": item.get("id"),
                        "location": item.get("location"),
                        "hashtags": item.get("caption").get("hashtags"),
                        "likes_count": item.get("like_count"),
                        "comment_count": item.get("comment_count"),
                        "created_at": item.get("caption").get("created_at"),
                    }
                )

            csvCreator(extracted_post_data, postSchema, "./csv/instagram/post.csv")
            return extracted_post_data
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")


def youtubeUserVideosScraper(channel_id: str):
    headers = {
        "x-rapidapi-key": youtubeApiKey,
        "x-rapidapi-host": youtubeApiHost,
    }

    querystring = {
        "part": "snippet,id",
        "key": youtubeKey,
        "channelId": channel_id,
        "maxResults": "50",
        "regionCode": "In",
        "relevanceLanguage": "hi",
        "type": "video",
    }

    response = requests.get(
        youtubeApiUrl + "/search", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            extracted_user_video_data = []
            for item in data["items"]:
                extracted_user_video_data.append(
                    {
                        "video_id": item["id"]["videoId"],
                        "channel_id": item["snippet"]["channelId"],
                        "title": item["snippet"]["title"],
                        "publishedAt": item["snippet"]["publishedAt"],
                    }
                )
            csvCreator(
                extracted_user_video_data,
                searched_youtube_user_video_Schema,
                "./csv/youtube/searched_user_videos.csv",
            )

            print("Youtube User's Videos are Scraped")

            filtered_user_videos_ids = csv_to_list(
                "./csv/youtube/searched_user_videos.csv", "video_id"
            )

            # print("filtered_user_videos_ids", filtered_user_videos_ids)
            youtubeVideoDataScraper(filtered_user_videos_ids)

        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")


def youtubeVideoDataScraper(video_ids: list[str]):
    headers = {
        "x-rapidapi-key": youtubeApiKey,
        "x-rapidapi-host": youtubeApiHost,
    }

    querystring = {
        "part": " id,  localizations,  snippet, statistics, status,  topicDetails",
        "key": "AIzaS9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6a7b8c9dTr",
        "id": video_ids,
        "regionCode": "In",
    }

    response = requests.get(
        youtubeApiUrl + "/videos", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            extracted_videos_data = []
            for item in data["items"]:
                extracted_videos_data.append(
                    {
                        "post_id": item["id"],
                        "location": "",
                        "hashtags": '',
                        "likes_count": item["statistics"]["likeCount"],
                        "comment_count": item["statistics"]["commentCount"],
                        "created_at": item["snippet"]["publishedAt"],
                    }
                )
            csvCreator(extracted_videos_data, postSchema, "./csv/youtube/post.csv")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")
