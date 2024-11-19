import yt_dlp

# ydl_opts = {
#     'outtmpl': 'josh',
#     'format': 'm4a/bestaudio/best',
#     'postprocessors': [{  # Extract audio using ffmpeg
#         'key': 'FFmpegExtractAudio',
#         'preferredcodec': 'm4a',
#     }],
# }

def get_playlist_videos(url):
    # Define the options for yt-dlp
    ydl_opts = {
        'quiet': True,  # Suppress output to keep it clean
        'extract_flat': True,  # Only get video information, don't download
        'force_generic_extractor': True,  # Force generic extractor for consistent output
    }

    urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)  # Extract info without downloading

        if 'entries' in info_dict:
            videos = info_dict['entries']
            for video in videos:
                urls.append((video['url'], video['duration']))
        else:
            urls.append((url, info_dict['duration']))

    return urls
