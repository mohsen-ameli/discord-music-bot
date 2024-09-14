import yt_dlp

def get_playlist_videos(playlist_url):
    # Define the options for yt-dlp
    ydl_opts = {
        'quiet': True,  # Suppress output to keep it clean
        'extract_flat': True,  # Only get video information, don't download
        'force_generic_extractor': True,  # Force generic extractor for consistent output
    }

    urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(playlist_url, download=False)  # Extract info without downloading

        if 'entries' in info_dict:
            videos = info_dict['entries']
            for video in videos:
                urls.append((video['url'], video['duration']))

    return urls
