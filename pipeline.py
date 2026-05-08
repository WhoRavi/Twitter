"""
Pipeline: search X -> filter & rank -> Grok rewrite -> auto-post.

Usage:
    python pipeline.py                  # dry-run (shows what would be posted)
    python pipeline.py --post           # actually post the top candidate
    python pipeline.py --post --top 3   # post top 3 (rate-limited)
"""

import argparse
import hashlib
import json
import os
import sys
import time
from urllib import error, parse, request

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from post import post_tweet, refresh_access_token  # reuse posting logic

BEARER_TOKEN = os.getenv("BEARER_TOKEN")
USER_ACCESS_TOKEN = os.getenv("USER_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")
XAI_API_KEY = os.getenv("XAI_API_KEY")

ROOT = os.path.dirname(os.path.abspath(__file__))
TOPICS_PATH = os.path.join(ROOT, "topics.json")
POSTED_PATH = os.path.join(ROOT, "posted.json")

X_SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
XAI_URL = "https://api.x.ai/v1/chat/completions"


# ---------- helpers ----------

def load_json(path: str, default):
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def http_json(method: str, url: str, *, headers: dict, body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = request.Request(url=url, data=data, headers=headers, method=method)
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        msg = exc.read().decode("utf-8") if exc.fp else exc.reason
        raise RuntimeError(f"{exc.code} {exc.reason}: {msg}") from exc


# ---------- 1. search X ----------

def search_x(query: str, max_results: int) -> list[dict]:
    if not BEARER_TOKEN:
        raise RuntimeError("BEARER_TOKEN missing in .env")
    url = f"{X_SEARCH_URL}?{parse.urlencode({
        'query': query,
        'max_results': max(10, min(max_results, 100)),
        'tweet.fields': 'created_at,public_metrics,lang,author_id',
    })}"
    result = http_json("GET", url, headers={"Authorization": f"Bearer {BEARER_TOKEN}"})
    return result.get("data", []) or []


# ---------- 2. filter & rank ----------

def score_post(post: dict, cfg: dict) -> int:
    text = post.get("text", "").lower()
    metrics = post.get("public_metrics", {})

    # Hard excludes
    for word in cfg["exclude_keywords"]:
        if word.lower() in text:
            return -1

    # Min engagement
    likes = metrics.get("like_count", 0)
    retweets = metrics.get("retweet_count", 0)
    if likes < cfg["min_likes"]:
        return -1

    # Boost score
    boost = sum(2 for w in cfg["boost_keywords"] if w.lower() in text)
    return likes + retweets * 2 + boost * 5


def gather_candidates(cfg: dict) -> list[dict]:
    seen_ids = set()
    candidates = []
    for query in cfg["search_queries"]:
        print(f"  search: {query[:80]}...")
        try:
            posts = search_x(query, cfg["results_per_query"])
        except RuntimeError as exc:
            print(f"    ! search failed: {exc}")
            continue
        for p in posts:
            if p["id"] in seen_ids:
                continue
            seen_ids.add(p["id"])
            score = score_post(p, cfg)
            if score < 0:
                continue
            p["_score"] = score
            candidates.append(p)
        time.sleep(1)  # gentle on rate limit
    candidates.sort(key=lambda p: p["_score"], reverse=True)
    return candidates


# ---------- 3. Grok rewrite ----------

def rewrite_with_grok(source_text: str, cfg: dict) -> str:
    if not XAI_API_KEY:
        raise RuntimeError("XAI_API_KEY missing in .env")

    user_msg = (
        f"Source post:\n\"\"\"\n{source_text}\n\"\"\"\n\n"
        f"Stance: {cfg['stance']}\n"
        f"Allowed hashtags: {' '.join(cfg['hashtags'])}\n"
        f"Max length: {cfg['max_post_length']} characters.\n\n"
        f"Write ONE tweet commenting on the source post. Output only the tweet."
    )
    body = {
        "model": cfg["grok_model"],
        "messages": [
            {"role": "system", "content": cfg["grok_system_prompt"]},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.7,
    }
    result = http_json("POST", XAI_URL, headers={
        "Authorization": f"Bearer {XAI_API_KEY}",
        "Content-Type": "application/json",
    }, body=body)
    text = result["choices"][0]["message"]["content"].strip()
    # strip wrapping quotes if Grok adds them
    if (text.startswith('"') and text.endswith('"')) or (text.startswith("'") and text.endswith("'")):
        text = text[1:-1].strip()
    # enforce length
    if len(text) > cfg["max_post_length"]:
        text = text[: cfg["max_post_length"] - 1].rstrip() + "…"
    return text


# ---------- 4. dedup ----------

def dedup_key(post: dict) -> str:
    # Use source tweet id as the dedup key
    return hashlib.sha1(post["id"].encode()).hexdigest()


# ---------- 5. main ----------

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post", action="store_true", help="Actually post (otherwise dry-run)")
    parser.add_argument("--top", type=int, default=1, help="Number of tweets to post")
    args = parser.parse_args()

    cfg = load_json(TOPICS_PATH, None)
    if cfg is None:
        sys.exit("topics.json not found")

    posted = load_json(POSTED_PATH, {"ids": []})
    posted_ids = set(posted["ids"])

    print("Step 1: searching X...")
    candidates = gather_candidates(cfg)
    print(f"  -> {len(candidates)} candidates after filter")

    fresh = [c for c in candidates if dedup_key(c) not in posted_ids]
    print(f"  -> {len(fresh)} after dedup")
    if not fresh:
        sys.exit("No fresh candidates. Try again later or relax filters.")

    selected = fresh[: args.top]
    print(f"\nStep 2: rewriting top {len(selected)} with Grok ({cfg['grok_model']})...\n")

    for i, src in enumerate(selected, 1):
        metrics = src.get("public_metrics", {})
        print(f"=== Candidate {i}/{len(selected)}  score={src['_score']}  likes={metrics.get('like_count')} ===")
        print(f"SOURCE: {src['text']}")
        try:
            tweet = rewrite_with_grok(src["text"], cfg)
        except RuntimeError as exc:
            print(f"! Grok failed: {exc}")
            continue
        print(f"REWRITE ({len(tweet)} chars): {tweet}\n")

        if not args.post:
            print("(dry-run, not posting)\n")
            continue

        access_token = USER_ACCESS_TOKEN
        try:
            result = post_tweet(tweet, access_token)
        except RuntimeError as exc:
            if "401" in str(exc) and REFRESH_TOKEN:
                print("Refreshing token...")
                access_token, _ = refresh_access_token(REFRESH_TOKEN)
                result = post_tweet(tweet, access_token)
            else:
                print(f"! Post failed: {exc}")
                continue

        tweet_id = result.get("data", {}).get("id")
        print(f"POSTED: https://x.com/i/web/status/{tweet_id}\n")
        posted_ids.add(dedup_key(src))
        save_json(POSTED_PATH, {"ids": list(posted_ids)})
        time.sleep(2)  # spacing between posts


if __name__ == "__main__":
    main()
