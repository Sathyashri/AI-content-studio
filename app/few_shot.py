import pandas as pd
import random

df = pd.read_csv("data/clean_posts.csv")

posts = df["text"].tolist()

def get_examples(n=3):
    return random.sample(posts, n)