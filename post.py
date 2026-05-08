"""
Minimal X API posting script.
Stdlib only. OAuth 2.0 PKCE for user-context POST /2/tweets.

Usage:
    1. First run:  python post.py
       - Prints an authorization URL.
       - Open it, approve, you'll be redirected to your Callback URL with ?code=... in the address bar.
       - Paste that `code` value when prompted.
       - Script exchanges it for an access token and saves it to .env.
       - Then it posts a sample tweet.
    2. Later runs: python post.py "your tweet text"
       - Reuses the saved token (auto-refreshes if expired) and posts immediately.
"""

import base64
import hashlib
import json
import os
import re
import secrets
import sys
from urllib import error, parse, request

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "https://www.examples.com")
USER_ACCESS_TOKEN = os.getenv("USER_ACCESS_TOKEN")
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN")

AUTH_URL = "https://x.com/i/oauth2/authorize"
TOKEN_URL = "https://api.x.com/2/oauth2/token"
TWEETS_URL = "https://api.x.com/2/tweets"
SCOPES = ["tweet.read", "tweet.write", "users.read", "offline.access"]
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _basic_header() -> str:
    return base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("ascii")


def _post_form(url: str, form: dict) -> dict:
    req = request.Request(
        url=url,
        data=parse.urlencode(form).encode("utf-8"),
        headers={
            "Authorization": f"Basic {_basic_header()}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8") if exc.fp else exc.reason
        raise RuntimeError(f"{exc.code} {exc.reason}: {body}") from exc


def update_env(updates: dict) -> None:
    """Write or replace KEY=VALUE entries in .env."""
    text = ""
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8") as f:
            text = f.read()
    for key, value in updates.items():
        line = f"{key}={value}"
        pattern = rf"(?m)^#?\s*{re.escape(key)}=.*$"
        if re.search(pattern, text):
            text = re.sub(pattern, line, text)
        else:
            text = text.rstrip() + f"\n{line}\n"
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(text)


def run_oauth_flow() -> tuple[str, str | None]:
    """Interactive OAuth 2.0 PKCE flow. Returns (access_token, refresh_token)."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise RuntimeError("CLIENT_ID and CLIENT_SECRET must be set in .env")

    code_verifier = _b64url(secrets.token_bytes(32))
    code_challenge = _b64url(hashlib.sha256(code_verifier.encode()).digest())
    state = secrets.token_urlsafe(16)

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": " ".join(SCOPES),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    print("\n=== Step 1: Open this URL in your browser and approve the app ===\n")
    print(f"{AUTH_URL}?{parse.urlencode(params)}\n")
    print("After approving, you'll be redirected to your Callback URL.")
    print("Look at the address bar — copy the value of the `code` query parameter.\n")

    raw = input("Paste the `code` value (or the full callback URL): ").strip()
    if not raw:
        raise RuntimeError("No code provided")

    # Accept either a bare code or the full redirected URL
    if raw.startswith("http://") or raw.startswith("https://") or raw.startswith("?"):
        qs = raw.split("?", 1)[-1]
        params_back = parse.parse_qs(qs)
        code = (params_back.get("code") or [""])[0]
        returned_state = (params_back.get("state") or [""])[0]
        if returned_state and returned_state != state:
            raise RuntimeError(f"State mismatch: expected {state!r}, got {returned_state!r}")
    else:
        code = raw

    if not code:
        raise RuntimeError("Could not find `code` in the input")

    print("\nExchanging code for access token...")
    payload = _post_form(TOKEN_URL, {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "code_verifier": code_verifier,
    })

    access_token = payload["access_token"]
    refresh_token = payload.get("refresh_token")
    update_env({
        "USER_ACCESS_TOKEN": access_token,
        "REFRESH_TOKEN": refresh_token or "",
    })
    print("Saved USER_ACCESS_TOKEN (and REFRESH_TOKEN) to .env")
    return access_token, refresh_token


def refresh_access_token(refresh_token: str) -> tuple[str, str | None]:
    payload = _post_form(TOKEN_URL, {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
    })
    access_token = payload["access_token"]
    new_refresh = payload.get("refresh_token", refresh_token)
    update_env({
        "USER_ACCESS_TOKEN": access_token,
        "REFRESH_TOKEN": new_refresh,
    })
    return access_token, new_refresh


def post_tweet(text: str, access_token: str) -> dict:
    req = request.Request(
        url=TWEETS_URL,
        data=json.dumps({"text": text}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8") if exc.fp else exc.reason
        raise RuntimeError(f"{exc.code} {exc.reason}: {body}") from exc


def main() -> None:
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello from my X API minimal script"

    access_token = USER_ACCESS_TOKEN
    refresh_token = REFRESH_TOKEN

    if not access_token:
        access_token, refresh_token = run_oauth_flow()

    print(f"\nPosting: {text!r}")
    try:
        result = post_tweet(text, access_token)
    except RuntimeError as exc:
        # If unauthorized and we have a refresh token, try once more
        if "401" in str(exc) and refresh_token:
            print("Access token expired. Refreshing...")
            access_token, refresh_token = refresh_access_token(refresh_token)
            result = post_tweet(text, access_token)
        else:
            raise

    print("\nSuccess!")
    print(json.dumps(result, indent=2))
    tweet_id = result.get("data", {}).get("id")
    if tweet_id:
        print(f"\nView: https://x.com/i/web/status/{tweet_id}")


if __name__ == "__main__":
    main()
