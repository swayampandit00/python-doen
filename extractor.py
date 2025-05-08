import os
import json


def extract_format_data(format_data):
    extension = format_data["ext"]
    format_name = format_data["format"]
    url = format_data["url"]
    return {
        "extension": extension,
        "format_name": format_name,
        "url": url
    }


def extract_video_data_from_url(url):
    command = f'yt-dlp "{url}" -j --no-playlist'
    output = os.popen(command).read()
    if not output:
        raise ValueError("No output from yt-dlp command. Possibly invalid URL or network issue.")
    try:
        video_data = json.loads(output)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON output from yt-dlp: {e}")
    title = video_data.get("title")
    formats = video_data.get("formats", [])
    thumbnail = video_data.get("thumbnail")
    formats = [extract_format_data(format_data) for format_data in formats]
    return {
        "title": title,
        "formats": formats,
        "thumbnail": thumbnail
    }
