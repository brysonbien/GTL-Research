#Import statements
import json
import csv
from googleapiclient.discovery import build

#Api Key generated 
api_key = 'AIzaSyDIuQ0gDsXrKNvGIdKMWUezUjkD9Kgrx8s'

csv_output = 'query_responses.csv'

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
def csvOutputVideos():
    print("####################################\n" + "COLLECTING VIDEO IDS\n" + "####################################")
    #Iterate through the keyword list to search youtube api and write out to query_responses.txt
    videoIds = {}
    for string in keyword_list:
        request = youtube.search().list(part="snippet",
                                        type='video',
                                        q = string,
                                        maxResults = 2)
        response = request.execute()

        nextPageToken = response["nextPageToken"]

        for elem in response['items']:
            videoId = elem["id"]["videoId"]
            publishedAt = elem["snippet"]["publishedAt"]
            channelId = elem["snippet"]["channelId"]
            title = elem["snippet"]["title"] 

            videoObject =  [title, 
                            publishedAt, 
                            channelId, 
                            nextPageToken]

            videoIds[videoId] = videoObject
    
    print("####################################\n" + "SAVING VIDEO IDS\n" + "####################################")

    with open(csv_output, 'w+') as f:
        f.write(",".join([  "topic",
                            "title",
                            "publishedAt",
                            "videoId",
                            "channelId",
                            "nextPageToken"]))
    with open(csv_output, 'a') as f:
        for vidId in videoIds.keys():
            f.write("\n" +
                    ",".join([videoIds[vidId][0],
                              videoIds[vidId][1],
                              vidId,
                              videoIds[vidId][2],
                              videoIds[vidId][nextPageToken]]))
                              
"""
Gets video statistics from video ID
"""
def getStatistics():
    print("####################################\n" + "VIDEO_IDS USED FOR STATS\n" + "####################################")
    
    
    with open('query_responses.csv', 'r') as f:
        data = f.read()
        split_data = data.split(",")
        split_data.reverse()
        print("\n")
        for videoId in split_data:
            request = youtube.videos().list(
                part = "id, statistics",
                id = videoId
                )
            response = request.execute()
            print(response["items"][0]["id"])
            print(response["items"][0]["statistics"])
            print("\n")
    print("\n")

"""
Iterate through the keyword list to search youtube api and write out to query_responses.csv
"""
def csvOutputComments():
    print("####################################\n" + "VIDEO_IDS USED FOR COMMENTS\n" + "####################################")
    with open('query_responses.csv', 'r') as f:
            data = f.read()
            split_data = data.split(",")
            split_data.reverse()
            for video_Id in split_data:
                print("\n" + video_Id)
                request = youtube.commentThreads().list(
                    videoId = video_Id,
                    part = "snippet,replies",
                    order = "relevance",
                    maxResults = 50
                    )
                try:
                    response = request.execute()
                    for elem in response['items']:
                        print("\n" + elem['snippet']['topLevelComment']['snippet']['textDisplay'])
                    print('\n')
                except:
                    print(video_Id + " has comments disabled, or something else went wrong")
    print("\n")

def main():
        csvOutputVideos()
        # csvOutputComments()
        # getStatistics()
main()