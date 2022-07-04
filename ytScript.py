#Import statements
import json
import csv
from googleapiclient.discovery import build

#Api Key generated 
api_key = 'AIzaSyDIuQ0gDsXrKNvGIdKMWUezUjkD9Kgrx8s'

csv_output = 'videoIdAndStats.csv'
comments_output = 'comments.csv'

#Building Youtube object
youtube = build('youtube', 'v3', developerKey=api_key)

#List of keywords
keyword_list = ["Computer Science Lists",
                # "Computer Science Stacks",
                # "Computer Science Queues",
                # "Computer Science Linked Lists",
                # "Computer Science Trees, AVL & Binary Trees",
                # "Computer Science Graphs",
                # "Computer Science Trees",
                # "Computer Science Hashing and hash tables",
                # "Computer Science Dynamic Programming",
                # "Computer Science Data Structures",
                # "Computer Science Algorithms"
                ]
                
"""
Gets the videoIds of the imported search parameters, stores them in a csv file.
It then uses those CSV to get the top 50 comments for each video.
"""
def getVideos(topic):
    #Iterate through the keyword list to search youtube api and write out to query_responses.txt
    videoIds = {}
    request = youtube.search().list(part="snippet",
                                    type='video',
                                    q = topic,
                                    maxResults = 2)
    response = request.execute()

    nextPageToken = response["nextPageToken"]

    for elem in response['items']:
        videoId = elem["id"]["videoId"]
        publishedAt = elem["snippet"]["publishedAt"]
        channelId = elem["snippet"]["channelId"]
        title = elem["snippet"]["title"] 

        videoObject =  [topic,
                        title, 
                        publishedAt, 
                        channelId, 
                        nextPageToken]

        videoIds[videoId] = videoObject
    return videoIds
                              
"""
Gets video statistics from video IDs

"statistics": {
    "viewCount": unsigned long,
    "likeCount": unsigned long,
    "dislikeCount": unsigned long,
    "favoriteCount": unsigned long,
    "commentCount": unsigned long
  }

"""
def getStatistics(videoIds):
    videoStats = {}
    for videoId in videoIds.keys():
            request = youtube.videos().list(part = "id, statistics",
                                            id = videoId
                                            )
            response = request.execute()

            videoStats[videoId] = response["items"][0]["statistics"]
    return videoStats

"""
Iterate through the keyword list to search youtube api and write out to query_responses.csv
"""
def getComments(videoIds):
    videoComments = {}
    for video_Id in videoIds:

        request = youtube.commentThreads().list(videoId = video_Id,
                                                part = "snippet,replies",
                                                order = "relevance",
                                                maxResults = 50)
        try:
            response = request.execute()
            for elem in response['items']:
               videoComments[video_Id] = elem['snippet']['topLevelComment']['snippet']['textDisplay']
        except:
            print(video_Id + " has comments disabled, or something else went wrong")
    print("\n")

"""
Gets channel statistics from channel ID
"""
def getChannelStats():
    print("####################################\n" + "CHANNEL_IDS USED FOR STATS\n" + "####################################")
    with open('query_responses.csv', 'r') as f:
        data = f.read()
        split_data = data.split(",")
        split_data.reverse()
        print("\n")
        for channelId in split_data:
            request = youtube.channels().list(
                part = "id, statistics",
                id = channelId
                )
            response = request.execute()
            print(response["items"][0]["id"])
            print(response["items"][0]["statistics"])
            print("\n")
    print("\n")

def main():
        #Gather Video Stats
        with open(csv_output, 'w+') as f:
            f.write(",".join([  "topic",
                                "title",
                                "publishedAt",
                                "videoId",
                                "channelId",
                                "viewCount",
                                "likeCount",
                                "favoriteCount",
                                "commentCount",
                                "nextPageToken"]))
        
        with open(comments_output, 'w+') as f:
            f.write(",".join([  "topic",
                                "title",
                                "publishedAt",
                                "videoId",
                                "channelId",
                                "viewCount",
                                "likeCount",
                                "favoriteCount",
                                "commentCount",
                                "nextPageToken"]))
        

        for topic in keyword_list:
            print("\n####################################\n" + "COLLECTING VIDEO IDS FOR " + topic + "\n####################################")
            videoIds = getVideos(topic)
            print("\n####################################\n" + "VIDEO_IDS USED FOR STATS FOR " + topic + "\n####################################")
            stats = getStatistics(videoIds)
            print("\n####################################\n" + "VIDEO_IDS USED FOR COMMENTS FOR " + topic + "\n####################################")
            #comments = getComments(videoIds)
            print("\n####################################\n" + "SAVING VIDEO IDS\n" + "####################################")

            with open(csv_output, 'a') as f:
                for vidId in videoIds.keys():
                    f.write("\n" +
                            ",".join([videoIds[vidId][0],
                                    videoIds[vidId][1],
                                    videoIds[vidId][2],
                                    vidId,
                                    videoIds[vidId][3],
                                    stats[vidId]['viewCount'],
                                    stats[vidId]['likeCount'],
                                    stats[vidId]['favoriteCount'],
                                    stats[vidId]['commentCount'],
                                    videoIds[vidId][4]]))

            print("\n####################################\n" + "SAVING COMMENTS\n" + "####################################")

                                    

main()