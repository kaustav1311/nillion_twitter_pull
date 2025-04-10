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

def get_latest_tweets(user_id, count=3):
    url = f"https://api.twitter.com/2/users/{user_id}/tweets"
    params = {
        "max_results": count,
        "tweet.fields": "created_at,attachments,referenced_tweets",
        "expansions": "attachments.media_keys",
        "media.fields": "url,preview_image_url,type",
         "exclude": "replies"
    }
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()
    return res.json()

def map_media(media_list):
    return {media["media_key"]: media for media in media_list}

def save_as_json(api_response, username):
    tweets = api_response["data"]
    media_map = map_media(api_response.get("includes", {}).get("media", []))
    today = datetime.utcnow().strftime("%Y%m%d")
    output_path = f"public/community_feed/twitter_{today}.json"
    output = []

    for tweet in tweets:
        # Skip retweets
        if "referenced_tweets" in tweet:
            if any(ref["type"] == "retweeted" for ref in tweet["referenced_tweets"]):
                continue

        tweet_media = []
        if "attachments" in tweet:
            for key in tweet["attachments"].get("media_keys", []):
                media_item = media_map.get(key)
                if media_item and media_item["type"] == "photo":
                    tweet_media.append(media_item.get("url"))
                elif media_item and "preview_image_url" in media_item:
                    tweet_media.append(media_item.get("preview_image_url"))

        output.append({
            "date": tweet["created_at"][:10],
            "source": "twitter",
            "author": f"@{username}",
            "text": tweet["text"],
            "link": f"https://twitter.com/{username}/status/{tweet['id']}",
            "media": tweet_media
        })

    os.makedirs("public/community_feed", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"✅ Saved {len(output)} tweets to {output_path}")

if __name__ == "__main__":
    user_id = get_user_id(USERNAME)
    api_response = get_latest_tweets(user_id)
    save_as_json(api_response, USERNAME)
