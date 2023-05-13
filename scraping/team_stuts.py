
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import mysql.connector
import datetime
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

list = []


for own_team_id in team_ids:
    url = 'https://www.bleague.jp/record/?club1=' + str(own_team_id[0]) + '&club2=0'

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # 必要な情報を取得する
    match_results = soup.find_all('div', {'class': 'record-match-result'})

    # 各試合の情報を表示する
    for match in match_results:
        home_tag = match.find('div', {'class': 'record-match-result-tag label home font-blg'})
        away_tag = match.find('div', {'class': 'record-match-result-tag label away font-blg'})

        if home_tag is not None:
            home_team_str = home_tag.text.strip()
            home_team = 1
        else:
            home_team_str = away_tag.text.strip()
            home_team = 0

        other_team_id = match.find('a', {'class': 'team text-link'})['href'].split('=')[-1]
        date_str = match.find('div', {'class': 'record-match-result-date font-blg'}).text.strip().replace('\n', '')
        result = match.find('div', {'class': 'record-match-result-winOrLose font-blg'})
        win_div = result.find('div', {'class': 'record-match-result-win font-blg'})
        if win_div is not None:
            win_or_lose_str = win_div.text.strip()
        else:
            lose_div = result.find('div', {'class': 'record-match-result-lose font-blg'})
            if lose_div is not None:
                win_or_lose_str = lose_div.text.strip()
            else:
                win_or_lose_str = ''
        own_score_str = result.find('div', {'class': 'record-match-result-score font-blg'}).text.strip().split('-')[0]
        other_score_str = result.find('div', {'class': 'record-match-result-score font-blg'}).text.strip().split('-')[1]
        
        # Home teamとWin or loseを整数型に変換する
        home_or_away = 1 if home_team_str == 'HOME' else 0
        win_or_lose = 1 if win_or_lose_str == 'WIN' else 0
        
        # 日付をPythonの日付型に変換する
        date = datetime.datetime.strptime(date_str, '%Y.%m.%d')
        
        # スコアを整数型に変換する
        own_score = int(own_score_str)
        other_score = int(other_score_str)
        # print(date, own_team_id[0], other_team_id, own_score, other_score,  win_or_lose, home_or_away)

        list.append([date, own_team_id[0], int(other_team_id), own_score, other_score,  win_or_lose, home_or_away])
    
    print(list)
    time.sleep(10)


for d in list:
    sql = "INSERT INTO bleague_analysis_game (date, own_team_id, other_team_id, own_score, other_score,  win_or_lose, home_or_away, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s,  CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
    print(d)
    mycursor.execute(sql, d)

mydb.commit()
mydb.close()