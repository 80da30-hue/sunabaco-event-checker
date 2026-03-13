import os
import requests
from bs4 import BeautifulSoup
import json

url = "https://sunabaco.com/event/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

titles = [t.text.strip() for t in soup.select(".eventCard__name")]

# 重複削除
titles = list(dict.fromkeys(titles))

# events.json を読み込む
try:
    with open("sunabaco-checker/events.json") as f:
        old_events = json.load(f)
except:
    old_events = []

# 新イベント
new_events = [t for t in titles if t not in old_events]

print("新イベント:")
for e in new_events:
    print(e)

# Slack通知
webhook_url = os.environ["SLACK_WEBHOOK_URL"]

for event in new_events:
    message = {
        "text": f"🎉 新しいSUNABACOイベントがあります！\n{event}\nhttps://sunabaco.com/event/"
    }
    requests.post(webhook_url, json=message)
name: Check SUNABACO Events

on:
  schedule:
    - cron: '0 1 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  run-script:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - run: pip install requests beautifulsoup4

      - run: python sunabaco-checker/check_events.py
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}

      - name: Commit updated events.json
        run: |
          git config --global user.name "github-actions"
          git config --global user.email "actions@github.com"
          git add sunabaco-checker/events.json
          git commit -m "Update events.json" || echo "No changes"
          git push

          # Slackテスト通知
webhook_url = os.environ["SLACK_WEBHOOK_URL"]

test_message = {
    "text": "SUNABACOイベントチェッカーのテスト通知です"
}

requests.post(webhook_url, json=test_message)


# events.json 更新
with open("sunabaco-checker/events.json", "w") as f:
    json.dump(titles, f)
