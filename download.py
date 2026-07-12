import requests
import os
import json

search_url = "https://api.modrinth.com/v2/search"
params = {
    "query": "pvp",
    "facets": json.dumps([
        ["project_type:resourcepack"],
        ["versions:1.19"],
        ["categories:combat"],
        ["categories:32x"]
    ]),
    "index": "downloads",
    "limit": 50
}

resp = requests.get(search_url, params=params)
resp.raise_for_status()
data = resp.json()

print(f"Total hits: {data['total_hits']}")
for hit in data["hits"]:
    print(f"{hit['title']} | {hit['slug']} | {hit['project_id']} | {hit['downloads']} downloads")

project_ids = [hit["project_id"] for hit in data["hits"]]


OUT_DIR = "D:\\alex's folder\\code\\mcproj\\data"
os.makedirs(OUT_DIR, exist_ok=True)

for pid in project_ids:
    versions = requests.get(f"https://api.modrinth.com/v2/project/{pid}/version").json()
    match = next((v for v in versions if "1.19" in v.get("game_versions", [])), None)

    if not match:
        print(f"No 1.19 version found for {pid}, skipping.")
        continue

    file = match["files"][0]
    filename = file["filename"]
    url = file["url"]

    print(f"Downloading {filename}...")
    r = requests.get(url)
    r.raise_for_status()
    with open(os.path.join(OUT_DIR, filename), "wb") as f:
        f.write(r.content)

print("Done.")