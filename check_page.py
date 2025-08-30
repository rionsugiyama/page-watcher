import requests
from bs4 import BeautifulSoup

URL = "https://www.31sumai.com/attend/X1413/"
STATUS_FILE = "last_status.txt"

def get_status():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")
    # とりあえず全文を取得（必要なら対象要素だけ抜き出す）
    return soup.get_text()

def main():
    status = get_status()

    try:
        with open(STATUS_FILE, "r") as f:
            old_status = f.read().strip()
    except FileNotFoundError:
        old_status = ""

    if status != old_status:
        print("ページが更新されました！")
        with open(STATUS_FILE, "w") as f:
            f.write(status)
    else:
        print("変化なし")

if __name__ == "__main__":
    main()
