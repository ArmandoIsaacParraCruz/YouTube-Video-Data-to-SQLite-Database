import sys
import googleapiclient.discovery
import dateutil.parser
import my_database

API_KEY = 'DEVELOPER_KEY'

# Create a YouTube API service
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY)

# Prompt the user to enter a search term
topic = input("Enter the term to search for: ")

# Display order types for sorting the search results
print('''Order types to sort the list:
date – Resources are sorted in reverse chronological order based on the date they were created.
rating – Resources are sorted from highest to lowest rating.
relevance – Resources are sorted based on their relevance to the search query. This is the default value for this parameter.
title – Resources are sorted alphabetically by title.
videoCount – Channels are sorted in descending order of their number of uploaded videos.
viewCount – Resources are sorted from highest to lowest number of views. For live broadcasts, videos are sorted by the number of concurrent viewers while the broadcasts are ongoing.
''')

# Prompt the user to choose the order type for sorting
order_param = input("Enter order type (date, rating, relevance, title, videoCount, viewCount): ")

# Prompt the user to enter the maximum number of results to retrieve
max_result = abs(int(input("Enter the number of results you want, max = 50: ")))

# Limit the number of results to a maximum of 50
if max_result > 50:
    max_result = 50

try:
    # Perform the YouTube API search with the specified parameters
    query_videos_ids = youtube.search().list(
        part="id",
        type='video',
        regionCode="US",
        order=order_param,
        q=topic,
        maxResults=max_result,
        fields="items(id(videoId))"
    ).execute()
except:
    print("Error while performing the query: query_videos_ids")
    sys.exit()

print("\nResults of the query:\n")
count = 0

# Create the database
my_database.create_database()

# Loop through each video ID in the search results
for item in query_videos_ids['items']:
    count += 1
    vid_id = item['id']['videoId']
    
    # Request video statistics and snippet data
    response = youtube.videos().list(
        part="statistics,snippet",
        id=vid_id
    ).execute()

    try:
        # Extract video details: title, publish datetime, view count, like count, comment count, video URL, and channel name
        video_title = response['items'][0]['snippet']['title']
        published_at = response['items'][0]['snippet']['publishedAt']
        published_datetime = dateutil.parser.parse(published_at)
        datetime_iso8601 = published_datetime.strftime('%Y-%m-%d %H:%M:%S')
        view_count = int(response['items'][0]['statistics']['viewCount'])
        like_count = int(response['items'][0]['statistics']['likeCount'])
        comment_count = int(response['items'][0]['statistics']['commentCount'])
        video_url = f"https://www.youtube.com/watch?v={vid_id}"
        channel_id = response['items'][0]['snippet']['channelId']
        
        # Get the channel name associated with the channel ID
        channel_response = youtube.channels().list(
            part='snippet',
            id=channel_id
        ).execute()
        channel_name = channel_response['items'][0]['snippet']['title']
        
        # Insert the video details into the database
        my_database.insert_record(video_title, datetime_iso8601, view_count, like_count, comment_count, video_url, channel_name)
        
        # Print the details of the video
        print(count, 'video name:', video_title)
        print("Channel name:", channel_name)
        print("Views:", view_count)
        print("Likes:", like_count)
        print("#comments:", comment_count)
        print(video_url)
        print('Publish datetime:', datetime_iso8601)
        print()
    except:
        # Continue to the next video if an error occurs while processing the current video
        print("Error processing a video")
        continue

# Close the database connection
my_database.close_database()




