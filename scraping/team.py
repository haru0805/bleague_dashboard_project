import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import mysql.connector

url = 'https://www.bleague.jp/club/?tab=1'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


team_id_links = soup.find_all('a', href=re.compile("TeamID=\d+"))

team_ids = []
for link in team_id_links:
    match = re.search("TeamID=(\d+)", link['href'])
    if match:
        team_id = match.group(1)
        if team_id not in team_ids:
            team_ids.append(team_id)

team_names = soup.find_all('div', class_='club-box-team')
team_locations = soup.find_all('div', class_='club-box-prefecture')

list = []
for team_name, team_id, locations in zip(team_names, team_ids, team_locations):
    list.append((team_id, team_name.get_text(strip=True), locations.get_text(strip=True)))

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Haru0805haru",
  database="teams"
)

mycursor = mydb.cursor()

# sql = 'insert into bleague_analysis_district (id, name, created_at, updated_at) VALUES (0, "未設定", CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)'
# mycursor.execute(sql)

for d in list:
    sql = "INSERT INTO bleague_analysis_team (bleague_id, name, location, created_at, updated_at) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    print(d)
    # mycursor.execute(sql, d)


mydb.commit()
mydb.close()