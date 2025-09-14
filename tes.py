

import json


with open("data.json", "r") as f:
    data = json.load(f)
    print(data)
list_video = data["content"]


export = "filtered_videos.json"

data =[]
for video in list_video:
    url= "http://27.72.62.135:5080/media/content/" + video["filename"]
    data.append({"video_url": url})



with open(export, "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)