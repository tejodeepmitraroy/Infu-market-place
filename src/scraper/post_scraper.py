import requests
import os
from dotenv import load_dotenv
from src.schemas.post_schema import postSchema
from src.utils.csv_creator import csvCreator
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


def instagramUserPostScraper(user):
    headers = {
        "x-rapidapi-key": instagramApiKey,
        "x-rapidapi-host": instagramApiHost,
    }

    querystring = {"username_or_id_or_url": user}

    response = requests.get(
        instagramApiUrl + "/v1.2/posts", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()

        if "data" in data:

            extracted_data = []

            for item in data["data"]["items"]:
                extracted_data.append(
                    {
                        "post_id": item.get("id"),
                        "location": item.get("location"),
                        "hashtags": item.get("caption").get("hashtags"),
                        "likes_count": item.get("like_count"),
                        "comment_count": item.get("comment_count"),
                    }
                )

            csvCreator(extracted_data, postSchema, "./csv/instagram/post.csv")
        else:
            print("No data found in the response.")
    else:
        print("Request failed with status code {response.status_code}")


def youtubeUserPostScraper():
    headers = {
        "x-rapidapi-key": youtubeApiKey,
        "x-rapidapi-host": youtubeApiHost,
    }

    querystring = {
        "part": "snippet",
        "key": youtubeKey,
        "channelType": "any",
        "eventType": "completed",
        "location": "28.66447, 77.18728",
        "locationRadius": "100km",
        "maxResults": "50",
        "regionCode": "In",
        "type": "video",
    }

    response = requests.get(
        youtubeApiUrl + "/search", headers=headers, params=querystring
    )

    if response.status_code == 200:
        data = response.json()
        print(data)

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
            csvCreator(extracted_data, postSchema, "./csv/youtube/post.csv")

    else:
        print("Request failed with status code {response.status_code}")

    # if response.status_code == 200:
    #     data = response.json()

    #     if "data" in data:

    #         extracted_data = []

    #         for item in data["data"]["items"]:
    #             extracted_data.append(
    #                 {
    #                     "post_id": item.get("id"),
    #                     "location": item.get("location"),
    #                     "likes_count": item.get("like_count"),
    #                     "comment_count": item.get("comment_count"),
    #                 }
    #             )

    #         # csvCreator(extracted_data, postSchema, ".src/csv/youtube/user.csv")

    #         df = pd.DataFrame(extracted_data, columns=postSchema)
    #         df.to_csv("./csv/instagram/post.csv", index=False)
    #         print("CSV file created successfully.")
    #     else:
    #         print("No data found in the response.")
    # else:
    #     print("Request failed with status code {response.status_code}")
