import feedparser
import pandas as pd
from bs4 import BeautifulSoup

tags = [
    "career",
    "productivity",
    "startup",
    "entrepreneurship",
    "artificial-intelligence",
    "machine-learning",
    "technology"
]

posts = []

for tag in tags:
    url = f"https://medium.com/feed/tag/{tag}"
    feed = feedparser.parse(url)

    for entry in feed.entries:
        clean_text = BeautifulSoup(entry.summary, "html.parser").get_text()

        posts.append({
            "tag": tag,
            "title": entry.title,
            "post": clean_text
        })

df = pd.DataFrame(posts)

df.to_csv("data/medium_posts.csv", index=False)

print("Posts collected:", len(df))