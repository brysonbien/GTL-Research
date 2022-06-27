#Import statements
import json
from googleapiclient.discovery import build

#Api Key generated 
api_key = 'AIzaSyDIuQ0gDsXrKNvGIdKMWUezUjkD9Kgrx8s'

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


#Iterate through the keyword list to search youtube api and write out to query_responses.txt
for string in keyword_list:
    request = youtube.search().list(
    part="snippet",
    type='video',
    q = string,
    maxResults = 2
    )

    response = request.execute()

# Reads videoIds from response .json document and writes to a new file
with open('query_responses.csv', 'w') as f:
    videoIds = []
    for elem in response['items']:
        videoIds.append(elem["id"]["videoId"])
    f.write(','.join(videoIds))