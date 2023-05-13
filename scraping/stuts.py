import requests
from bs4 import BeautifulSoup
import re
import mysql.connector
import time

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="Haru0805haru",
#   database="teams"
# )

# mycursor = mydb.cursor()


# sql = "select bleague_id from bleague_analysis_team;"
# mycursor.execute(sql)
# team_ids = mycursor.fetchall()


from requests_html import HTMLSession

url = "https://www.bleague.jp/roster_detail/?PlayerID=8467"

# セッション開始
session = HTMLSession()
r = session.get(url)

# ブラウザエンジンでHTMLを生成させる
r.html.render()

# id が 'scores' の tbody 要素を取得
tbody_element = r.html.find('tbody#scores', first=True)

# tbody 要素の中のすべての tr 要素を取得
tr_elements = tbody_element.find('tr')

# 各 tr 要素の中の td 要素を取得して表示
for tr in tr_elements:
    td_elements = tr.find('td')
    row_values = [td.text for td in td_elements]
    print(', '.join(row_values))