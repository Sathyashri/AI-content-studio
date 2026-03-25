import requests
import pandas as pd
import time

tags = [
    "career",
    "productivity",
    "startup",
    "entrepreneurship",
    "ai",
    "machinelearning",
    "technology",
    "programming",
    "python"
]

posts = []

for tag in tags:

    print("Collecting:", tag)

    for page in range(1, 30):

        url = f"https://dev.to/api/articles?tag={tag}&page={page}"

        r = requests.get(url)

        data = r.json()

        if len(data) == 0:
            break

        for article in data:

            posts.append({
                "tag": tag,
                "title": article["title"],
                "post": article["description"]
            })

        time.sleep(0.5)

df = pd.DataFrame(posts)

df.drop_duplicates(inplace=True)

df.to_csv("data/devto_posts.csv", index=False)

print("Total posts collected:", len(df))