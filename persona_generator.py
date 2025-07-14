import os
import requests
from dotenv import load_dotenv
import praw
load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def test_connection(username):
    user = reddit.redditor(username)
    print(f"Connected! Redditor found: u/{user.name}")

def fetch_user_activity(username, limit=50):
    user = reddit.redditor(username)
    posts, comments = [], []

    print(f"Fetching posts and comments for u/{username}...")
    for submission in user.submissions.new(limit=limit):
        posts.append({
            "title": submission.title,
            "text": submission.selftext,
            "url": f"https://reddit.com{submission.permalink}"
        })
    for comment in user.comments.new(limit=limit):
        comments.append({
            "text": comment.body,
            "url": f"https://reddit.com{comment.permalink}"
        })

    print(f"Fetched {len(posts)} posts and {len(comments)} comments.\n")
    return posts, comments

def generate_persona_from_activity(username, posts, comments):
    print(f"Generating persona for u/{username}...")

    content = "USER POSTS:\n"
    for post in posts:
        content += f"- Title: {post['title']}\nText: {post['text']}\nSource: {post['url']}\n\n"

    content += "\nUSER COMMENTS:\n"
    for comment in comments:
        content += f"- Comment: {comment['text']}\nSource: {comment['url']}\n\n"

    prompt = f"""
You are a UX researcher. Based on the following Reddit posts and comments, generate a detailed user persona for u/{username} with:
- Name
- Age
- Gender
- Occupation
- Personality
- Motivations
- Frustrations
- Archetype
- Behavior online

❗CITE at least one Reddit URL for each trait from the data provided.

Here is the Reddit activity:
{content}
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    if response.status_code == 200:
        print("Persona generation complete.")
        return response.json()["response"]
    else:
        print("Error generating persona.")
        print(response.text)
        return "Failed to generate persona."
def save_persona_to_file(username, persona_text):
    output_dir = "sample_users"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{username}.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"Persona saved to: {output_path}")
if __name__ == "__main__":
    username = "LeadPersonal7959"
    test_connection(username)
    posts, comments = fetch_user_activity(username)
    persona = generate_persona_from_activity(username, posts, comments)
    save_persona_to_file(username, persona)