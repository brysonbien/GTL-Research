#Import statements
import json
from googleapiclient.discovery import build

#Api Key generated 
api_key = 'AIzaSyBYoNWt_KjSIYSQYo55j2nXf_3_oD9N29k'

#Building Youtube object
youtube = build('youtube', 'v3', developerKey=api_key)

#List of keywords
keyword_list = []
keyword_list.append("Computer Science Lists")
keyword_list.append("Computer Science Stacks")
keyword_list.append("Computer Science Queues")
keyword_list.append("Computer Science Linked Lists")
keyword_list.append("Computer Science Trees, AVL & Binary Trees ")
keyword_list.append("Computer Science Graphs")
keyword_list.append("Computer Science Trees")
keyword_list.append("Computer Science Hashing and hash tables")
keyword_list.append("Computer Science Dynamic Programming")
keyword_list.append("Computer Science Data Structures")
keyword_list.append("Computer Science Algorithms")

#File path with type "write"
f = open("query_responses.txt", 'w')

#Iterate through the keyword list to search youtube api and write out to query_responses.txt
for string in keyword_list:
    request = youtube.search().list(
    part="snippet",
    type='video',
    q = string,
    maxResults = 10
    )

    with open("query_responses.txt", 'a') as f:
        response = request.execute()
        #See yotube api request in terminal
            #print(response)
        json.dump(response, f, indent=4)

# Reads videoIds from response .txt document and writes to a new file
with open('query_videoIds.txt','w') as n:

with open('query_responses.txt') as f:
    content = f.read()

    d = json.load(f)
    videoIds = []
    for elem in d['items']:
        videoIds.append(elem["id"]["videoId"])

json.dump(videoIds, n, indent=4)