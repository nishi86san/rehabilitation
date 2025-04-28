import requests
from bs4 import BeautifulSoup
import re

# アクセスするURL
url = "https://news.yahoo.co.jp"

# URL にアクセスする
res = requests.get(url)

# res.textをbeautifulSoupで扱うための処理
soup = BeautifulSoup(res.content, "html.parser")

# href属性に特定の文字列が含まれているリンクを検索
elems = soup.find_all('a', href=True)

# 特定の文字列(pickup)が含まれているリンクをフィルタリング
for elem in elems:
    href = elem['href']
    if re.search("news.yahoo.co.jp/pickup", href):
        print(f"記事タイトル: {elem.get_text(strip=True)}")
        print(f"記事URL: {href}")
        print(f"-----")

