#Import statements
from datetime import datetime
import json
import csv
from googleapiclient.discovery import build
import os

#Api Key generated 
api_key = 'AIzaSyAnrZsLVr_DHWjIaGUVA7u1PsQ75VEzz3c'

video_output = 'videoIdAndStats.tsv'
comments_output = 'comments.tsv'
channel_output = 'channel.tsv'

#Parameters
NUM_OF_VIDEOS = 30
NUM_OF_COMMENTS = 50

#Building Youtube object
youtube = build('youtube', 'v3', developerKey=api_key)

#List of keywords
keyword_list = ["Computer Science Lists",
                "Computer Science Stacks"
                "Computer Science Queues",
                "Computer Science Linked Lists",
                "Computer Science Trees AVL Binary Trees",
                "Computer Science Graphs",
                "Computer Science Trees",
                "Computer Science Hashing and hash tables",
                "Computer Science Dynamic Programming",
                "Computer Science Data Structures",
                "Computer Science Algorithms"
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
                                    maxResults = NUM_OF_VIDEOS)
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
                                                textFormat = "plainText",
                                                maxResults = NUM_OF_COMMENTS)
        try:
            response = request.execute()
            topLevelComments = []
            for elem in response['items']:
                topLevelComments.append(elem['snippet']['topLevelComment']['snippet'])
            videoComments[video_Id] = topLevelComments
        except:
            print(video_Id + " has comments disabled, or something else went wrong")
            videoComments[video_Id] = None
    return videoComments

"""
Gets channel statistics from channel ID
"""
def getChannelStats(videoIds):
    channelStats = {}
    for videoID in videoIds.keys():
        channelId = videoIds[videoID][3]
        request = youtube.channels().list(
            part = "id, statistics",
            id = channelId
            )
        response = request.execute()
        channelStats[channelId] = response["items"][0]["statistics"]
    return channelStats

def main():
        #Gather Video Stats
        with open(video_output, 'w+') as f:
            f.write("\t".join([  "topic",
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
            f.write("\t".join([  "topic",
                                "videoId",
                                "authorchannelID",
                                "authorDisplayName",
                                "textOriginal",
                                "likeCount",
                                "publishedAt",
                                "updatedAt"]))

        with open(channel_output, 'w+') as f:
            f.write("\t".join([ "topic",
                                "title",
                                "publishedAt",
                                "channelId",
                                "viewCount",
                                "subscriberCount",
                                "videoCount",
                                ]))
        

        for topic in keyword_list:

            compiledJson = {}
            compiledJson['topic'] = topic
            compiledJson['videos'] = {}
            compiledJson['channels'] = {}

            print("\n####################################\n" + "COLLECTING VIDEO IDS FOR " + topic + "\n####################################")
            videoIds = getVideos(topic)
            print("\n####################################\n" + "VIDEO_IDS USED FOR STATS FOR " + topic + "\n####################################")
            stats = getStatistics(videoIds)
            print("\n####################################\n" + "VIDEO_IDS USED FOR COMMENTS FOR " + topic + "\n####################################")
            comments = getComments(videoIds)
            print("\n####################################\n" + "VIDEO_IDS USED FOR CHANNELS " + topic + "\n####################################")
            channels = getChannelStats(videoIds)


            print("\n####################################\n" + "SAVING VIDEO IDS\n" + "####################################")
            with open(video_output, 'a') as f:
                for vidId in videoIds.keys():
                    try:
                        f.write("\n" +
                                "\t".join([topic,
                                        videoIds[vidId][1],
                                        videoIds[vidId][2],
                                        vidId,
                                        videoIds[vidId][3],
                                        stats[vidId]['viewCount'],
                                        stats[vidId]['likeCount'],
                                        stats[vidId]['favoriteCount'],
                                        stats[vidId]['commentCount'],
                                        videoIds[vidId][4]]))
                        compiledJson['videos'][vidId] = {"topic": topic,
                                                        "title": videoIds[vidId][1],
                                                        "publishedAt": videoIds[vidId][2],
                                                        "videoId": vidId,
                                                        "channelId": videoIds[vidId][3],
                                                        "viewCount": stats[vidId]['viewCount'],
                                                        "likeCount": stats[vidId]['likeCount'],
                                                        "favoriteCount": stats[vidId]['favoriteCount'],
                                                        "commentCount": stats[vidId]['commentCount'],
                                                        "nextPageToken": videoIds[vidId][4]
                                                        }
                        compiledJson['videos'][vidId]['comments'] = {}
                    except:
                        print(vidId + " has likes disabled, or something else went wrong")
                        stats[vidId] = None

            print("\n####################################\n" + "SAVING COMMENTS\n" + "####################################")
            with open(comments_output, 'a') as f:
                for vidId in videoIds.keys():
                    if(comments[vidId] is not None):
                        commentsList = []
                        for comment in comments[vidId]:
                            f.write("\n" +
                                    "\t".join([topic,
                                            vidId,
                                            videoIds[vidId][3],
                                            comment['authorChannelId']['value'],
                                            comment['authorDisplayName'],
                                            comment['textOriginal'].replace('\n', ' '),
                                            str(comment['likeCount']),
                                            comment['publishedAt'],
                                            comment['updatedAt']]))
                            
                            commentsList.append({"topic": topic,
                                                            "videoId": vidId,
                                                            "channelId": videoIds[vidId][3],
                                                            "authorDisplayName": comment['authorChannelId']['value'],
                                                            "textOriginal": comment['textOriginal'].replace('\n', ' '),
                                                            "likeCount": str(comment['likeCount']),
                                                            "publishedAt": comment['publishedAt'],
                                                            "updatedAt": comment['updatedAt']})
                        try:
                            compiledJson['videos'][vidId]['comments'] = commentsList
                        except:
                            print(vidId + " has likes disabled, or something else went wrong")
                        

            print("\n####################################\n" + "SAVING CHANNEL STATS\n" + "####################################")
            with open(channel_output, 'a') as f:
                for channelId in channels.keys():
                        if(not channels[channelId]['hiddenSubscriberCount']):
                            f.write("\n" +
                                "\t".join([topic,
                                        videoIds[vidId][1], 
                                        videoIds[vidId][2],
                                        channelId,
                                        channels[channelId]['viewCount'],
                                        channels[channelId]['subscriberCount'],
                                        channels[channelId]['videoCount']
                                        ]))
                        
                            compiledJson['channels'][channelId]= {  "topic": topic,
                                                                    "title": videoIds[vidId][1],
                                                                    "publishedAt": videoIds[vidId][2],
                                                                    "channelId": channelId,
                                                                    "viewCount": channels[channelId]['viewCount'],
                                                                    "subscriberCount": channels[channelId]['subscriberCount'],
                                                                    "videoCount": channels[channelId]['videoCount']}
            with open((topic.replace("Computer Science ", "")).replace(" ", "_") +'.json', 'w') as f:
                    f.write(json.dumps(compiledJson, indent = 4))

main()