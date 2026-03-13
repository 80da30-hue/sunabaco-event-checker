import requests
from bs4 import BeautifulSoup
import json

url = "https://sunabaco.com/event/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

titles = [t.text.strip() for t in soup.select(".eventCard__name")]

# 重複削除
titles = list(dict.fromkeys(titles))

try:
    with open("events.json") as f:
        old_events = json.load(f)
except:
    old_events = []

new_events = [t for t in titles if t not in old_events]

print("新イベント:")
for e in new_events:
    print(e)

with open("events.json", "w") as f:
    json.dump(titles, f)