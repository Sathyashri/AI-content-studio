import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

tags = [
    "career",
    "productivity",
    "startup",
    "entrepreneurship",
    "artificial-intelligence",
    "machine-learning",
    "technology"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

posts = []

for tag in tags:

    print("Collecting:", tag)

    url = f"https://medium.com/tag/{tag}/latest"

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    articles = soup.find_all("h2")

    for article in articles:
        title = article.get_text()

        posts.append({
            "tag": tag,
            "title": title,
            "post": title
        })

    time.sleep(1)

df = pd.DataFrame(posts)

df.drop_duplicates(inplace=True)

df.to_csv("data/medium_posts_large.csv", index=False)

print("Total posts:", len(df))