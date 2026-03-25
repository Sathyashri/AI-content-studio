import pandas as pd

df = pd.read_csv("data/devto_posts.csv")

df = df.dropna()

df["text"] = df["title"] + " " + df["post"]

df = df[["text"]]
df.to_csv("data/clean_posts.csv", index=False)

print("Clean posts:", len(df))