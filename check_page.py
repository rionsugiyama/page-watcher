import requests
from bs4 import BeautifulSoup
import hashlib
import os

URL = "https://www.31sumai.com/attend/X1413/"
STATE_FILE = "last_hash.txt"

def get_page_hash(url):
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text()
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_last_hash():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return None

def save_last_hash(h):
    with open(STATE_FILE, "w") as f:
        f.write(h)

def notify_line(message: str):
    token = os.getenv("LINE_TOKEN")
    if not token:
        print("LINE_TOKEN が設定されていません")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "to": "Udeadbeefdeadbeefdeadbeefdeadbeef",  # ダミー
        "messages": [{"type": "text", "text": message}]
    }

    # 実際は "/v2/bot/message/broadcast" を使えば全員に送れる
    response = requests.post(
        "https://api.line.me/v2/bot/message/broadcast",
        headers=headers,
        json={"messages": [{"type": "text", "text": message}]}
    )
    if response.status_code != 200:
        print("LINE送信エラー:", response.text)

def main():
    current_hash = get_page_hash(URL)
    last_hash = load_last_hash()

    if last_hash is None:
        print("初回チェック：ハッシュを保存しました。")
        save_last_hash(current_hash)
        return

    if current_hash != last_hash:
        msg = f"ページが更新されました！\n{URL}"
        print(msg)
        notify_line(msg)  # Bot経由でLINE通知
        save_last_hash(current_hash)
    else:
        print("変化なし。")

if __name__ == "__main__":
    main()
