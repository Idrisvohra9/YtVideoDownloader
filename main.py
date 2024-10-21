import yt_dlp
from tqdm import tqdm


def download_youtube_audio(video_url):
    try:

        def tqdm_progress_hook(d):
            if d["status"] == "downloading":
                file_size = d.get("total_bytes", 0)
                progress = tqdm(
                    total=file_size, unit="B", unit_scale=True, desc=d["filename"]
                )
                progress.update(d.get("downloaded_bytes", 0))

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": "music/%(title)s.%(ext)s",
            "progress_hooks": [tqdm_progress_hook],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        print("Downloaded successfully")
    except Exception as e:
        print(f"Error occurred: {str(e)}")


# Example usage
if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_audio(video_url)
