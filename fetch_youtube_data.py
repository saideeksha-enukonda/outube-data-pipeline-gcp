from googleapiclient.discovery import build
import pandas as pd

# Replace with your API Key
API_KEY = "AIzaSyCbkb4Wx4DERwtH3KFgUuWhrupSNBwwDcg"

# Initialize YouTube API
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_videos(channel_id):
    """Fetches videos from a specific YouTube channel."""
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=10,  # Number of videos to fetch
        order="date"
    )
    response = request.execute()

    videos = []
    for item in response["items"]:
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        published_at = item["snippet"]["publishedAt"]
        
        # Fetch video statistics
        stats = youtube.videos().list(
            part="statistics",
            id=video_id
        ).execute()
        
        if "items" in stats and stats["items"]:
            views = stats["items"][0]["statistics"].get("viewCount", 0)
            likes = stats["items"][0]["statistics"].get("likeCount", 0)
            comments = stats["items"][0]["statistics"].get("commentCount", 0)
        else:
            views, likes, comments = 0, 0, 0

        videos.append([video_id, title, published_at, views, likes, comments])

    return pd.DataFrame(videos, columns=["Video_ID", "Title", "Published_At", "Views", "Likes", "Comments"])

# Replace with a YouTube Channel ID (e.g., TEDx Talks: UCsT0YIqwnpJCM-mx7-gSA4Q)
channel_id = "UCEW_Fg9lQ2VaS7DLVma01Cg"

# Fetch data and save as CSV
df = get_videos(channel_id)
df.to_csv("youtube_videos.csv", index=False)

print("YouTube video data saved successfully!")
