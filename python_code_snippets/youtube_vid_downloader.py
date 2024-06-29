import yt_dlp

# Enter the URL for the download
url = input("Enter URL: ")
ydl_opts = {}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("video downloaded successfully")