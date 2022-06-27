#Import statements
import json
import csv
from googleapiclient.discovery import build

#Api Key generated 
api_key = 'AIzaSyDIuQ0gDsXrKNvGIdKMWUezUjkD9Kgrx8s'

"""
Iterate through the keyword list to search youtube api and write out to query_responses.csv
"""
def csvOutputVideos(youtube, string):
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
def csvOutputComments(youtube, videoID):
    request = youtube.commentThreads().list(
        videoID = videoID,
        part = "snippet,replies",
        order = "relevance",
        maxResults = 50
        )
    response = request.execute()
    with open('query_responses.csv', 'a') as f:
        videoIds = []
        for elem in response['items']:
            videoIds.append(elem["id"]["videoId"])
        f.write(','.join(videoIds))

"""
Gets the videoIds of the imported search parameters, stores them in a csv file.
It then uses those CSV to get the top 50 comments for each video.
"""
class Main:
    def __main__():
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
        for string in keyword_list:
            csvOutputVideos(youtube, string)
        for line in...
            csvOutputComments(youtube, videoID)

filename = 'file.csv'

with open(filename, 'r') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        print(row)
COPY
