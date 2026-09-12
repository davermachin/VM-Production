/* 
To run, a virtual environment is recommended. Install the required packages using:

python3 -m venv youtube-env
source youtube-env/bin/activate
python3 -m pip install requests

 then you can run via: python3 get_comments.py
*/

import csv
import requests

API_KEY = "AIzaSyCNh3zuiidSD63Bw3JF1q-IsVidB_mZNw4"
VIDEO_ID = "TwKjaH0lwrg"

BASE_URL = "https://www.googleapis.com/youtube/v3"


def get_top_level_comments():
    comments = []
    page_token = None

    while True:
        params = {
            "part": "snippet",
            "videoId": VIDEO_ID,
            "maxResults": 100,
            "textFormat": "plainText",
            "key": API_KEY,
        }

        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            f"{BASE_URL}/commentThreads",
            params=params
        )
        response.raise_for_status()
        data = response.json()

        for thread in data.get("items", []):
            snippet = thread["snippet"]
            comment = snippet["topLevelComment"]
            comment_snippet = comment["snippet"]

            comments.append({
                "comment_id": comment["id"],
                "parent_id": "",
                "author": comment_snippet.get("authorDisplayName", ""),
                "text": comment_snippet.get("textOriginal", ""),
                "published_at": comment_snippet.get("publishedAt", ""),
                "updated_at": comment_snippet.get("updatedAt", ""),
                "like_count": comment_snippet.get("likeCount", 0),
                "is_reply": False,
                "thread_reply_count": snippet.get("totalReplyCount", 0),
            })

            # Get ALL replies, if any
            reply_count = snippet.get("totalReplyCount", 0)

            if reply_count:
                comments.extend(
                    get_replies(comment["id"])
                )

        page_token = data.get("nextPageToken")

        if not page_token:
            break

    return comments


def get_replies(parent_id):
    replies = []
    page_token = None

    while True:
        params = {
            "part": "snippet",
            "parentId": parent_id,
            "maxResults": 100,
            "textFormat": "plainText",
            "key": API_KEY,
        }

        if page_token:
            params["pageToken"] = page_token

        response = requests.get(
            f"{BASE_URL}/comments",
            params=params
        )
        response.raise_for_status()
        data = response.json()

        for comment in data.get("items", []):
            snippet = comment["snippet"]

            replies.append({
                "comment_id": comment["id"],
                "parent_id": parent_id,
                "author": snippet.get("authorDisplayName", ""),
                "text": snippet.get("textOriginal", ""),
                "published_at": snippet.get("publishedAt", ""),
                "updated_at": snippet.get("updatedAt", ""),
                "like_count": snippet.get("likeCount", 0),
                "is_reply": True,
                "thread_reply_count": "",
            })

        page_token = data.get("nextPageToken")

        if not page_token:
            break

    return replies


comments = get_top_level_comments()

with open("youtube_comments.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "comment_id",
            "parent_id",
            "author",
            "text",
            "published_at",
            "updated_at",
            "like_count",
            "is_reply",
            "thread_reply_count",
        ]
    )

    writer.writeheader()
    writer.writerows(comments)

print(f"Downloaded {len(comments)} comments/replies.")
print("Saved to youtube_comments.csv")