import json
import requests
from bs4 import BeautifulSoup

# Setup
url = "https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/"
response = requests.get(url)
doc = BeautifulSoup(response.text, "html.parser")

title_tags = doc.select("h2.body-h2.css-18txe20.emt9r7s1")
titles = [title_tag.text for title_tag in title_tags]
# Select all <ul> tags with the matching class that contain <li> items
pickup_line_container_tags = [
    ul for ul in doc.select("ul.css-1wk73g0.emevuu60")
    if ul.select_one('li')
]
print(pickup_line_container_tags)
all_li = []

for pickup_line_container_tag in pickup_line_container_tags:
    # Select only <li> tags that have the attribute data-node-id
    li_tags = pickup_line_container_tag.select('ul.css-1wk73g0.emevuu60 > li[data-node-id]')
    
    all_pickup_lines_in_ul = [
        li.text.split('RELATED:')[0].strip()
        for li in li_tags
    ]
    
    all_li.append(all_pickup_lines_in_ul)

data = {}
for i in range(min(len(all_li), len(titles))):
    data[titles[i]] = all_li[i]

# Save the resulting dictionary to a JSON file
with open("pickup_lines.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("write data to pickup_lines.json successfully")