import os
import requests
import hashlib

URL = "https://www.31sumai.com/attend/X1413/"
LAST_HASH_FILE = "last_hash.txt"

# LINE通知用関数
def notify_line(message):
    token = os.getenv("LINE_TOKEN")
    if not token:
        print("LINE_TOKEN が設定されていません")
        return
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    r = requests.post("https://api.line.me/v2/bot/message/broadcast",
                      headers=headers, json={"messages":[{"type":"text","text":message}]})
    print("LINE通知ステータス:", r.status_code, r.text)

# ページのハッシュを取得
def get_page_hash():
    res = requests.get(URL)
    res.raise_for_status()
    return hashlib.sha256(res.text.encode("utf-8")).hexdigest()

def main():
    new_hash = get_page_hash()
    if os.path.exists(LAST_HASH_FILE):
        with open(LAST_HASH_FILE, "r") as f:
            last_hash = f.read().strip()
        if new_hash != last_hash:
            print("ページが更新されました！")
            notify_line("ページが更新されました！\n" + URL)
        else:
            print("変化なし。")
    else:
        print("初回チェック：ハッシュを保存しました。")

    # ハッシュを保存
    with open(LAST_HASH_FILE, "w") as f:
        f.write(new_hash)

if __name__ == "__main__":
    main()
