#Import statements
import json
import csv
from googleapiclient.discovery import build

#Api Key generated 
api_key = 'AIzaSyDIuQ0gDsXrKNvGIdKMWUezUjkD9Kgrx8s'

"""
Iterate through the keyword list to search youtube api and write out to query_responses.csv
"""
def csvOutputVideos(youtube, keyword_list):
    for string in keyword_list:
        request = youtube.search().list(
        part="snippet",
        type='video',
        q = string,
        maxResults = 2
        )

        response = request.execute()

        # Reads videoIds from response .json document and writes to a csv file
        with open('query_responses.csv', 'w') as f:
            videoIds = []
            for elem in response['items']:
                videoIds.append(elem["id"]["videoId"])
            f.write(','.join(videoIds))


# Gets Comments for each videoID in the CSV
def csvOutputComments(youtube):
     with open('query_responses.csv', 'r') as f:
            data = f.read()
            split_data = data.split(",")
            print(split_data)
            for video_Id in split_data:
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

"""
Gets the videoIds of the imported search parameters, stores them in a csv file.
It then uses those CSV to get the top 50 comments for each video.
"""
def main():
        #Building Youtube object
        youtube = build('youtube', 'v3', developerKey=api_key)

        #List of keywords
        keyword_list = []
        keyword_list.append("Computer Science Lists")
        # keyword_list.append("Computer Science Stacks")
        # keyword_list.append("Computer Science Queues")
        # keyword_list.append("Computer Science Linked Lists")
        # keyword_list.append("Computer Science Trees, AVL & Binary Trees ")
        # keyword_list.append("Computer Science Graphs")
        # keyword_list.append("Computer Science Trees")
        # keyword_list.append("Computer Science Hashing and hash tables")
        # keyword_list.append("Computer Science Dynamic Programming")
        # keyword_list.append("Computer Science Data Structures")
        # keyword_list.append("Computer Science Algorithms")
        csvOutputVideos(youtube, keyword_list)
        csvOutputComments(youtube)

main()
