

from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns


api_key = 'AIzaSyDkFXppfNQO2BGdZF1AXZ8OSjljU_LA3uA'
channel_ids = ['UCkGS_3D0HEzfflFnG0bD24A',
               'UCxmkk8bMSOF-UBF43z-pdGQ',
               'UCXgGY0wkgOzynnHvSEVmE3A',
               'UCNU_lfiiWBdtULKOw6X0Dig'
               ]

youtube = build('youtube', 'v3', developerKey=api_key)


def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name=response['items'][i]['snippet']['title'],
                    Subscriber=response['items'][i]['statistics']['subscriberCount'],
                    Views=response['items'][i]['statistics']['viewCount'],
                    Video_count=response['items'][i]['statistics']['videoCount'],
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    return all_data


channel_statistics = get_channel_stats(youtube, channel_ids)

channel_data = pd.DataFrame(channel_statistics)
print(channel_data)

channel_data['Subscriber'] = pd.to_numeric(channel_data['Subscriber'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Video_count'] = pd.to_numeric(channel_data['Video_count'])

# to compare who has the highest subscriber
sns.set(rc={'figure.figsize': (10, 8)})
ax = sns.barplot(x='Channel_name', y='Subscriber', data=channel_data)
print(ax)

# to compare who has most views
sns.set(rc={'figure.figsize': (10, 8)})
ax = sns.barplot(x='Channel_name', y='Views', data=channel_data)
print(ax)

# Function to get video IDs

playlist_id = channel_data.loc[channel_data['Channel_name'] == 'Hitesh Choudhary', 'playlist_id'].iloc[0]
#print(playlist_id)


def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50)

    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response['nextPageToken']
    more_page = True
    while more_page:
        if next_page_token is None:
            more_page = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')
    return (video_ids)


video_ids = get_video_ids(youtube, playlist_id)

def get_video_details(youtube,video_ids):
    all_video_stats = []
    for i in range(0,50):
           request = youtube.videos().list(
                     part = 'snippet,statistics',
                     id = ','.join(video_ids[:50]))
           response = request.execute()

           for video in response['items']:
               video_stats = dict(Title = video['snippet']['title'],
                                  Published_date = video['snippet']['publishedAt'],
                                  Views = video['statistics']['viewCount'],
                                  Likes = video['statistics']['likeCount'],
                                  Comments = video['statistics']['commentCount'])
               all_video_stats.append(video_stats)
    return (all_video_stats)

video_details = get_video_details(youtube,video_ids)

video_data = pd.DataFrame(video_details)


print(video_data)

