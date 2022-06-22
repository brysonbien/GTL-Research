from googleapiclient.discovery import build

api_key = 'AIzaSyBYoNWt_KjSIYSQYo55j2nXf_3_oD9N29k'

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.videos().list(
    part="snippet",
    q="data structures and algorithms",
    maxResults=2

)

response = request.execute()

print(response)

