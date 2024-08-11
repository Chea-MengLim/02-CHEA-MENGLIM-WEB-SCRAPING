import json

import requests
from bs4 import BeautifulSoup

url = "https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/"
response = requests.get(url)
doc = BeautifulSoup(response.text, "html.parser")

title_container = doc.select_one("div.css-1adm8f3.emt9r7s6 > ul.css-l03nee.emt9r7s4")
title_tags = title_container.findAll("li", class_="css-32630i emt9r7s3")

# store all titles in list
titles = []
for title in title_tags:
    titles.append(title.text)

pickup_line_containers = doc.find_all("ul", class_="css-1r2vahp emevuu60")
# remove ul if there is no li in it
for pickup_line_container in pickup_line_containers:
    if pickup_line_container.find("li") is None:
        pickup_line_containers.remove(pickup_line_container)

# store all pickup lines in list (2-dimensional list)
pickup_lines = []

for pickup_line_container in pickup_line_containers:
    pickup_lines_li = pickup_line_container.find_all("li")
    temp = []
    for pickup_line_li in pickup_lines_li:
        # if content inside li tag contain the word "RELATED:", I considered :
        # the content after the word "RELATED:" is not pickup line, so I need only the word before this word
        if "RELATED:" in pickup_line_li.text:
            temp.append(pickup_line_li.text.split("RELATED:")[0])
        else:
            temp.append(pickup_line_li.text)
    pickup_lines.append(temp)

# store data into json format
data = {}
for i in range(len(titles)):
    data[titles[i]] = pickup_lines[i]

# Write the JSON data to the file
file_name = 'data.json'
with open(file_name, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("Data has been saved successfully in file data.json")