import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.bleague.jp/stats/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')


team_id_links = soup.find_all('div', class_='player-b1')
print(soup)