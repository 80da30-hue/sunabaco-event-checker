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

# events.json 更新
with open("sunabaco-checker/events.json", "w") as f:
    json.dump(titles, f)
