import feedparser
import pandas as pd
from bs4 import BeautifulSoup
import time

tags = [
    "career",
    "productivity",
    "startup",
    "entrepreneurship",
    "artificial-intelligence",
    "machine-learning",
    "technology",
    "programming",
    "data-science",
    "leadership",
    "self-improvement",
    "coding",
    "python",
    "software-engineering"
]

posts = []

for tag in tags:

    print(f"Collecting posts from: {tag}")

    for page in range(0, 100):

        url = f"https://medium.com/feed/tag/{tag}"

        feed = feedparser.parse(url)

        for entry in feed.entries:

            clean_text = BeautifulSoup(entry.summary, "html.parser").get_text()

            posts.append({
                "tag": tag,
                "title": entry.title,
                "post": clean_text
            })

        time.sleep(0.5)

df = pd.DataFrame(posts)

df.drop_duplicates(inplace=True)

df.to_csv("data/medium_posts_large.csv", index=False)

print("Total posts collected:", len(df))