import os
import requests
from bs4 import BeautifulSoup
import json

url = "https://sunabaco.com/event/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

cards = soup.select(".eventCard")

events = []

for card in cards:
    title = card.select_one(".eventCard__name").text.strip()
    date = card.select_one(".eventCard__date").text.strip()
    link = card.select_one("a")["href"]

    event_text = f"{title} ({date})\n{link}"
    events.append(event_text)

# 重複削除
events = list(dict.fromkeys(events))

# events.json を読み込む
try:
    with open("sunabaco-checker/events.json") as f:
        old_events = json.load(f)
except:
    old_events = []

# 新イベント
new_events = [e for e in events if e not in old_events]

print("新イベント:")
for e in new_events:
    print(e)

# Slack通知
webhook_url = os.environ["SLACK_WEBHOOK_URL"]

for event in new_events:
    message = {
        "text": f"🎉 新しいSUNABACOイベントがあります！\n{event}"
    }
    requests.post(webhook_url, json=message)

# events.json 更新
with open("sunabaco-checker/events.json", "w") as f:
    json.dump(events, f)
