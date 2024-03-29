import requests
import os
from datetime import datetime
from bs4 import BeautifulSoup

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def upload_gitAction(data: str):
    try:
        token = os.environ.get('TOKEN')
        url = "https://api.github.com/repos/Pma10/MelonChartTop100/issues"
        response = requests.post(url, json={"title": f"{datetime.now().strftime('%Y년 %m월 %d일')} 멜론차트 TOP100", "body": data}, headers={"Authorization": f"token {token}"})
        response.raise_for_status()
        print('업로드 성공')
    except requests.exceptions.RequestException as e:
        print('업로드 실패:', e)

def get_melon_chart():
    try:
        melon100 = requests.get("https://www.melon.com/chart/index.htm", headers=header).text
        soup = BeautifulSoup(melon100, 'html.parser')
        titles = soup.select('div.ellipsis.rank01 > span')
        authors = soup.select('div.ellipsis.rank02 > span')
        return [title.text for title in titles], [author.text for author in authors]
    except requests.exceptions.RequestException as e:
        print('멜론 차트 데이터를 가져오는 데 실패했습니다:', e)
        return [], []

charts = []
with open(f'melon_chart/{datetime.now().strftime("%Y년%m월%d일")}.txt', 'a', encoding='utf-8') as f:
    titles, authors = get_melon_chart()
    for rank in range(len(titles)):
        title_name = titles[rank].replace('\n', '').strip()
        charts.append(f"TOP {rank + 1} {title_name} / {authors[rank]}\n")
        f.write(f"TOP {rank + 1} {title_name} / {authors[rank]}\n")

upload_gitAction("".join(charts))
