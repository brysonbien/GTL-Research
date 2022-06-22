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
    header = "\n#################################################\n" + "\n#################################################\n"+ string + "\n#################################################\n"+ "\n#################################################\n"

    with open("query_responses.txt", 'a') as f:
        response = request.execute()
        #See yotube api request in terminal
            #print(response)
        f.write(header)
        json.dump(response, f, indent=4)
