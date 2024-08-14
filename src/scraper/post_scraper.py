import requests
import os
from dotenv import load_dotenv
from src.schemas.post_schema import postSchema, searched_youtube_user_video_Schema
from src.utils.csv_creator import csvCreator
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
                        "user_id": user_id,
                        "location": item.get("location"),
                        "hashtags": (
                            item.get("caption").get("hashtags")
                            if item.get("caption")
                            else []
                        ),
                        "likes_count": item.get("like_count"),
                        "comment_count": item.get("comment_count"),
                        "created_at": (
                            item.get("caption").get("created_at")
                            if item.get("caption")
                            else None
                        ),
                    }
                )

            csvCreator(extracted_post_data, postSchema, "./csv/instagram/post.csv")
            return extracted_post_data
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")


def youtubeChannelVideosScraper(channel_id: str):
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
                    # item["id"].get("videoId")
                    {
                        "video_id": item["id"].get("videoId"),
                        "channel_id": item["snippet"].get("channelId"),
                        "title": item["snippet"].get("title"),
                        "publishedAt": item["snippet"].get("publishedAt"),
                    }
                )

            csvCreator(
                extracted_user_video_data,
                searched_youtube_user_video_Schema,
                "./csv/youtube/searched_user_videos.csv",
            )

            # print("Youtube Channel Videos are Scraped")

            # filtered_user_videos_ids = csv_to_list(
            #     "./csv/youtube/searched_user_videos.csv", "video_id"
            # )

            # # print("filtered_user_videos_ids===================>/n", filtered_user_videos_ids)

            # # if filtered_user_videos_ids:

            # # print(filtered_user_videos_ids)

            # edited_array_video_id=[]

            # for video_id in range(0,len(filtered_user_videos_ids)) :
            #     if(video_id % 20==0):
            #         youtubeVideoDataScraper(edited_array_video_id)
            #         edited_array_video_id=[]
            #     else:
            #         edited_array_video_id.append(filtered_user_videos_ids[video_id])

        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code", response.status_code)


def youtubeVideoDataScraper(video_ids: list[str]):
    # using a loop
    # avoiding printing last comma
    formatted_output = ""
    for i, element in enumerate(video_ids):
        formatted_output += element
        if i != len(video_ids) - 1:
            formatted_output += ","

    # print("The formatted output is : ", str(formatted_output))

    headers = {
        "x-rapidapi-key": youtubeApiKey,
        "x-rapidapi-host": youtubeApiHost,
    }

    querystring = {
        "part": " id, localizations, snippet, statistics, status, topicDetails",
        "key": youtubeKey,
        "id": str(formatted_output),
        "maxResults": "50",
        "regionCode": "In",
    }

    response = requests.get(
        youtubeApiUrl + "/videos", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()


        if "items" in data and len(data["items"]) != 0:
            # print("videos_data Data ========>", data["items"])
            extracted_videos_data = []
            
            for item in data["items"]:
                extracted_videos_data.append(
                    {
                        "post_id": item["id"],
                        "user_id": item["snippet"].get("channelId"),
                        "location": "",
                        "hashtags": item["snippet"].get("tags"),
                        "likes_count": item["statistics"].get("likeCount"),
                        "comment_count": item["statistics"].get("commentCount"),
                        "created_at": item["snippet"].get("publishedAt"),
                    }
                )

            print("extracted_videos_data Data ========>", extracted_videos_data)

            csvCreator(extracted_videos_data, postSchema, "./csv/youtube/post.csv")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code", response.status_code)
