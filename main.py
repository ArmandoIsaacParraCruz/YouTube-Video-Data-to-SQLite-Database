import sys
import googleapiclient.discovery
import dateutil.parser
import my_database

API_KEY = 'DEVELOPER_KEY'

api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=API_KEY)


topic = input("Enter the term to search for: ")

print('''Order types to sort the list:

date – Resources are sorted in reverse chronological 
order based on the date they were created.
		   
rating – Resources are sorted from highest to lowest rating.
	
relevance – Resources are sorted based on their relevance to 
the search query. This is the default value for this parameter.
				
title – Resources are sorted alphabetically by title.
	
videoCount – Channels are sorted in descending order of their number of uploaded videos.
	
viewCount – Resources are sorted from highest to lowest number of views. 
For live broadcasts, videos are sorted by number of concurrent viewers while 
the broadcasts are ongoing.

''')

order_param = input("Enter order type (date, rating, relevance, title, videoCount, viewCount): ")
max_result = abs(int(input("Enter the number of results you want, max = 50: ")))

if max_result > 50:
    max_result = 50

try:
    query_videos_ids = youtube.search().list(
        part="id",
        type='video',
        regionCode="US",
        order= order_param,
        q=topic,
        maxResults= max_result,
        fields="items(id(videoId))"
    ).execute()
except:
    print("Error while performing the query: query_videos_ids")
    sys.exit()

print("\nResults of the query:\n")
count = 0

my_database.create_database()

for item in query_videos_ids['items']:
    count += 1
    vid_id = item['id']['videoId']
    response = youtube.videos().list(
        part="statistics,snippet",
        id=vid_id
    ).execute()

    #try:
    # getting the title of the video
    video_title = response['items'][0]['snippet']['title']
        
    # getting the publish datetime
    published_at = response['items'][0]['snippet']['publishedAt']
    published_datetime = dateutil.parser.parse(published_at)
    datetime_iso8601 = published_datetime.strftime('%Y-%m-%d %H:%M:%S')
    
    # getting the view count
    view_count = int(response['items'][0]['statistics']['viewCount']) 
    
    # getting the like count
    like_count = int(response['items'][0]['statistics']['likeCount']) 
    
    # getting the comment count
    comment_count = int(response['items'][0]['statistics']['commentCount']) 
    
    #getting the url
    video_url = f"https://www.youtube.com/watch?v={vid_id}"
    
    # getting the channel name
    channel_id = response['items'][0]['snippet']['channelId']
    channel_response = youtube.channels().list(
        part='snippet',
        id=channel_id
    ).execute()
    channel_name = channel_response['items'][0]['snippet']['title']
    
    my_database.insert_record(video_title, datetime_iso8601, view_count, like_count,
                 comment_count, video_url, channel_name)
                 
    print(count, 'video name:', video_title)
    print("Channel name:", channel_name)
    print("Views:", view_count)
    print("Likes:", like_count)
    print("#comments:", comment_count)
    print(video_url)
    print('Publish datetime:', datetime_iso8601)
    print()
    #except:
    #    continue

my_database.close_database()




