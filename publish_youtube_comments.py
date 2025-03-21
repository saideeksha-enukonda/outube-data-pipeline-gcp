from googleapiclient.discovery import build
from google.cloud import pubsub_v1
import json
import time

# GCP Configuration
PROJECT_ID = "youtube-data-project-454318"
PUBSUB_TOPIC = "youtube-comments"

# YouTube API Configuration
API_KEY = "AIzaSyCbkb4Wx4DERwtH3KFgUuWhrupSNBwwDcg"
VIDEO_ID = "eK71EN3P78U"  # Replace with a trending video ID

# Initialize YouTube API Client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Initialize Pub/Sub Client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, PUBSUB_TOPIC)

def fetch_youtube_comments(video_id):
    """Fetches latest YouTube comments from a given video ID."""
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=10,  # Fetch latest 10 comments
        order="time"
    )
    response = request.execute()

    for item in response["items"]:
        comment_text = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comment_author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
        published_at = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]

        # Prepare message
        message_data = {
            "video_id": video_id,
            "author": comment_author,
            "comment": comment_text,
            "timestamp": published_at
        }

        # Publish to Pub/Sub
        message_json = json.dumps(message_data).encode("utf-8")
        publisher.publish(topic_path, message_json)
        print(f"Published comment: {comment_text}")

# Run every 10 seconds to get new comments
while True:
    fetch_youtube_comments(VIDEO_ID)
    time.sleep(10)
