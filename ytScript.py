import json

from googleapiclient.discovery import build

api_key = 'AIzaSyBYoNWt_KjSIYSQYo55j2nXf_3_oD9N29k'

youtube = build('youtube', 'v3', developerKey=api_key)

keyword_list = []
keyword_list.append("Computer Science Lists")
#keyword_list.append("Computer Science Stacks")
#keyword_list.append("Computer Science Queues")
#keyword_list.append("Computer Science Linked Lists")
#keyword_list.append("Computer Science Trees, AVL & Binary Trees ")
#keyword_list.append("Computer Science Graphs")
#keyword_list.append("Computer Science Tries")
#keyword_list.append("Computer Science Hashing and hash tables")
#keyword_list.append("Computer Science Dynamic Programming")
#keyword_list.append("Computer Science Data Structures")
#keyword_list.append("Computer Science Algorithms")

f = open("query_responses.txt", 'w')

for string in keyword_list:
    request = youtube.search().list(
    part="snippet",
    type='video',
    q = string,
    maxResults = 10
    )
    header = "#################################################\n"+ string + "\n#################################################\n"

    with open("query_responses.txt", 'w') as f:
        response = request.execute()
        #See yotube api request in terminal
            #print(response)
        f.write(header)
        json.dump(response, f, indent=4)
