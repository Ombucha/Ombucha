"""
This code uses the Unsplash API to randomly fetch a photo from their database.

Author: Omkaar Nerurkar
Date: 2025-06-06
"""


#######################
##### Web Service #####
#######################

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Welcome! You've arrived at the backend powering Omkaar's GitHub profile.")

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

def run_server():
    server = HTTPServer(('0.0.0.0', 8080), CustomHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()


###############################################
##### Unsplash and GitHub API Integration #####
###############################################

import os
import base64
import time
import requests
from datetime import datetime, timedelta, timezone

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
UNSPLASH_BASE_URL = "https://api.unsplash.com"
GITHUB_BASE_URL = "https://api.github.com"

while True:

    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    params = {"orientation": "landscape"}
    response = requests.get(f"{UNSPLASH_BASE_URL}/photos/random", headers=headers, params=params).json()

    if response.status_code == 200:

        image_url = response["urls"]["regular"]
        description = response.get("description", "")
        author_name = response["user"]["name"]
        author_username = response["user"]["username"]
        page_url = response["links"]["html"]

        headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
        response = requests.get(f"{GITHUB_BASE_URL}/repos/Ombucha/Ombucha/contents/README.md", headers=headers).json()
        sha = response["sha"]

        new_content = f"""# Omkaar's Image of the Hour

---

<div align="center">

<a href="{page_url}">
    <img src="{image_url}" alt="Image" style="max-width:100%; height:auto;">
</a>

<br>

<i>{description}</i>

</div>

---

**Photo by** [{author_name}](https://unsplash.com/@{author_username}) on Unsplash
"""
        encoded_content = base64.b64encode(new_content.encode()).decode()

        payload = {
            "message": "Update README (via API)",
            "content": encoded_content,
            "sha": sha,
            "committer": {
                "name": "github-actions[bot]",
                "email": "41898282+github-actions[bot]@users.noreply.github.com"
            }
        }
        response = requests.put(f"{GITHUB_BASE_URL}/repos/Ombucha/Ombucha/contents/README.md", headers=headers, json=payload)

    now = datetime.now(timezone.utc)
    next_hour = (now + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    wait_seconds = (next_hour - now).total_seconds()
    time.sleep(wait_seconds)