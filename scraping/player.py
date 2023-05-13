import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
import time

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Haru0805haru",
  database="teams"
)

mycursor = mydb.cursor()


sql = "select bleague_id from bleague_analysis_team;"
mycursor.execute(sql)
team_ids = mycursor.fetchall()


for team_id in team_ids:

    url = 'https://www.bleague.jp/club_detail/?TeamID=' + str(team_id[0]) + '&tab=2'
    print(url)

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    player_names = soup.find_all('div', class_='playerInfo-player-name')
    player_number = soup.find_all('div', class_='playerInfo-player-position')
    player_id = soup.find_all('a', class_='playerInfo-player')

    numbers = []

    for tag in player_number:
        text = tag.text
        number = re.search(r'#(\d+)', text)
        if number:
            numbers.append(int(number.group(1)))

    html_tags = soup.find_all('a', class_='playerInfo-player')

    player_ids = []

    for tag in html_tags:
        player_id = re.search(r'PlayerID=(\d+)', tag['href'])
        if player_id:
            player_ids.append(int(player_id.group(1)))

    list = []

    for player_name, number, id in zip(player_names, numbers, player_ids):
        list.append([str(id), player_name.get_text(strip=True), number, team_id[0], 0])

    for d in list:
        sql = "INSERT INTO bleague_analysis_player (bleague_id, name, number, team_id, position_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
        print(d)
        mycursor.execute(sql, d)
    time.sleep(10)

mydb.commit()
mydb.close()