import pandas as pd
from llm_helper import generate_from_llm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# load dataset
df = pd.read_csv("data/clean_posts.csv")
df = df.dropna(subset=["text"])

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# compute embeddings for all posts (only once)
post_embeddings = model.encode(df["text"].tolist())


def generate_post(topic):

    # embed user topic
    topic_embedding = model.encode([topic])

    # compute similarity
    similarities = cosine_similarity(topic_embedding, post_embeddings)[0]

    # get top 5 similar posts
    top_indices = similarities.argsort()[-5:][::-1]

    examples = df.iloc[top_indices]["text"].tolist()

    example_text = "\n\n".join(examples)

    prompt = f"""
You are a viral LinkedIn content creator.

Write a highly engaging LinkedIn post about: {topic}

Follow these LinkedIn writing rules:
- Start with a strong hook
- Use short sentences
- Use lots of white space
- Add 3 bullet points
- End with a motivational takeaway
- Add 3 hashtags

Here are similar LinkedIn posts for style reference:

{example_text}

Now generate a NEW LinkedIn post in the same style.
Do NOT copy the examples.
"""

    return generate_from_llm(prompt)