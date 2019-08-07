import requests
import json
import datetime
import sys
import os

BASE = "https://www.googleapis.com/youtube/v3/"
APP_KEY = "AIzaSyAp1nm1tf-Rz6zzkvnARKz8IEqSYIzqpSs"

def length_in_seconds(duration):
    coefs = [1, 60, 3600]
    duration_elems = [int(el) for el in reversed(duration.split(":"))]
    length = 0
    for i in range(len(duration_elems)):
        length += duration_elems[i]*coefs[i]
    return length


def main(NAME="music"):
    videos_list = []

    channels_list = []

    with open("channel lists/" + NAME+"_list.txt") as f:
        for line in f:
            channels_list.append(line.split()[0].strip())

    with open("last retrieved/" + NAME + "_last_retrieved.txt") as f:
        date_last_retrieved = f.read()

    for channel_id in channels_list:
        latest_videos = json.loads(requests.get(BASE + "search?part=snippet&channelId=" + channel_id + "&publishedAfter=" + date_last_retrieved + "&order=date&type=video&maxResults=50&key=" + APP_KEY).text)

        if len(latest_videos["items"]) > 0:
            ids_list = ""
            for item in latest_videos["items"]:
                ids_list += item["id"]["videoId"] + ","
            ids_list = ids_list[:-1]

            video_details = json.loads(requests.get(BASE + "videos?id=" + ids_list + "&part=contentDetails&key=" + APP_KEY).text)
            for i in range(len(video_details["items"])):
                duration = video_details["items"][i]["contentDetails"]["duration"]
                if 'S' not in duration:
                    duration += '0S'
                if 'M' not in duration and 'H' in duration:
                    duration = duration[:duration.find('H')+1] + '0M' + duration[duration.find('H')+1:]
                duration = duration.replace("H", ":").replace("M", ":").replace("S", "").replace("PT", "")
                duration = ":".join([elem if len(elem)==2 else "0"+elem for elem in duration.split(":")])
                latest_videos["items"][i]["duration"] = duration

            videos_list += latest_videos["items"]

    videos_list.sort(key=lambda x: length_in_seconds(x["duration"]), reverse=True)


    now = datetime.datetime.today()

    with open("last retrieved/" + NAME + "_last_retrieved.txt", 'w') as f:
        f.write(now.strftime("%Y-%m-%dT%H:%M:%SZ"))

    now_filename = now.strftime("%Y-%m-%d--%H-%M-%S")
    now = now.strftime("%d-%m-%Y--%H-%M-%S")

    wrapper = """<tr><td>
    <p>Channel: <a href=\"%s\">%s</a></p>
    <p>Title: <strong>%s</strong></p>
    <p>Duration: <strong>%s</strong>&nbsp;&nbsp;&nbsp;Published on: %s</p>
    <img src = %s alt = "Thumbnail Image" class="wrap align-left"/>%s
    <p>URL: <a href=\"%s\">%s</a></p>
    </td></tr>"""

    html_text = """<html>
    <head>
    <title>Newest Uploads - %s</title>
    <style>
    img { display: block; }
    img.wrap { max-width: 70%%; margin: 0px 0px; }
    img.align-left { float: left; margin-right: 30px; }
    </style>
    </head>
    <body>
    <h3>Newest Uploads - %s</h3>
    <table border = "1" cellpadding = "5" cellspacing = "5">""" % (now, now)

    for item in videos_list:
        channel = item["snippet"]["channelTitle"]
        channel_url = "https://www.youtube.com/channel/" + item["snippet"]["channelId"] + "/videos"
        title = item["snippet"]["title"]
        video_url = "https://www.youtube.com/watch?v=" + item["id"]["videoId"]
        thumb_url = item["snippet"]["thumbnails"]["default"]["url"]
        description = item["snippet"]["description"]
        duration = item["duration"]
        time_published = item["snippet"]["publishedAt"]
        time_published = time_published[:time_published.find('T')]
        html_text += wrapper % (channel_url, channel, title, duration, time_published, thumb_url, description, video_url, video_url)

    html_text += """</table></body>
    </html>"""

    if not os.path.exists("generated lists"):
        os.makedirs("generated lists")
    with open("generated lists/" + NAME + "_" + now_filename + ".html", 'w') as f:
        f.write(html_text.encode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
