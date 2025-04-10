# scripts/fetch_tweets.py

import os, requests, json
from datetime import datetime

BEARER_TOKEN = os.getenv("TWITTER_BEARER")
USERNAME = "nillionnetwork"

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

def get_user_id(username):
    url = f"https://api.twitter.com/2/users/by/username/{username}"
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json()['data']['id']

def get_latest_tweets(user_id, count=5):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": count,
        "tweet.fields": "created_at"
    }
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    return res.json()['data']

def save_as_json(tweets, username):
    today = datetime.utcnow().strftime("%Y%m%d")
    output_path = f"public/community_feed/twitter_{today}.json"
    output = [{
        "date": t["created_at"][:10],
        "source": "twitter",
        "author": f"@{username}",
        "text": t["text"],
        "link": f"https://twitter.com/{username}/status/{t['id']}"
    } for t in tweets]

    os.makedirs("public/community_feed", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"✅ Saved: {output_path}")

if __name__ == "__main__":
    user_id = get_user_id(USERNAME)
    tweets = get_latest_tweets(user_id)
    save_as_json(tweets, USERNAME)

