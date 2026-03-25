# ---------------- LINKEDIN PROMPT ----------------
def build_linkedin_prompt(topic, category, length):

    if length == "Short":
        length_instruction = "Write a concise post (80–120 words)."
    elif length == "Medium":
        length_instruction = "Write a balanced post (150–220 words)."
    else:
        length_instruction = "Write a detailed post (450–550 words)."

    prompt = f"""
You are an expert LinkedIn content creator.

Topic: {topic}
Category: {category}

{length_instruction}

STRICT RULES:
- ALWAYS include exactly 5 hashtags at the end (mandatory)
- Hashtags must be on a new line
- Do NOT skip hashtags under any condition
- Start directly with a powerful hook
- Use short, impactful paragraphs
- Include exactly 3 bullet points
- Add a strong ending
- Use simple and clear language
- Output ONLY the final post

FORMAT:

Hook

Paragraph

• Point 1  
• Point 2  
• Point 3  

Closing line

#tag1 #tag2 #tag3 #tag4 #tag5
"""
    return prompt


# ---------------- YOUTUBE TITLES PROMPT ----------------
def build_youtube_prompt(topic):

    prompt = f"""
Generate 8-10 engaging YouTube video titles.

Topic: {topic}

IMPORTANT:
- If the topic involves sensitive or violent themes, make it educational, documentary, or awareness-based
- Avoid harmful or graphic language
- Make titles curiosity-driven and clickable
- Keep titles short (under 12 words)

Output ONLY the titles as a list.
"""
    return prompt