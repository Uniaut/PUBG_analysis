import gzip
import json
from operator import truediv
import os
from textwrap import indent
import urllib.request
from chicken_dinner.pubgapi import PUBG


file_path = "seasonID/seasonID.json"
with open(file_path, "r") as f:
    seasonID_json = json.load(f)


# 현재 시즌중인 seasonId 찾기
for id in seasonID_json["data"]:
    if id["attributes"]["isCurrentSeason"]:
        seasonID = id["id"]


# 현재 진행 중인 시즌seasonID값을 가져와서  pc-as(아시아섭), solo(솔로3인칭) 리더보드 출력
req = urllib.request.Request(
    url=f"https://api.pubg.com/shards/pc-as/leaderboards/{seasonID}/solo",
    headers={
        "Authorization": f"Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiI2NzNlZGFhMC1hOWZlLTAxM2EtY2I4Ni0wMTM2YWI5NGY3N2IiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNjUxMjQ1ODc2LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6ImZyb3plbmRvZyJ9.mdDyb3P1KCBcNIk5xKeu7B7IWOIIaWpAc9JKL7TGyiY",
        "Accept": "application/vnd.api+json",
    },
)

file_name = f"leaderboard.json"
file_path = os.path.join("./leaderboard", file_name)
with urllib.request.urlopen(req) as response, open(file_path, "w") as write_file:
    json_data = json.loads(
        # gzip.decompress(response.read())
        response.read()
    )
    write_file.write(json.dumps(json_data, indent=4))
    print("saved.")
