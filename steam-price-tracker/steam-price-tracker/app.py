import requests
from bs4 import BeautifulSoup

def get_steam_price(game_name):
    # Steam 搜尋 URL 範例（以遊戲名稱搜尋）
    search_url = f"https://store.steampowered.com/search/?term={game_name}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }

    res = requests.get(search_url, headers=headers)
    if res.status_code != 200:
        return {"name": game_name, "current_price": "查無價格"}

    soup = BeautifulSoup(res.text, "html.parser")

    # 找搜尋結果第一筆遊戲
    game_item = soup.select_one("a.search_result_row")
    if not game_item:
        return {"name": game_name, "current_price": "查無價格"}

    # 遊戲名稱
    name = game_item.select_one(".title").text.strip()

    # 價格資訊（有折扣和無折扣兩種情況）
    price = "查無價格"
    discount_price = game_item.select_one(".search_price.discounted")
    if discount_price:
        # 折扣後價格，格式像 "NT$ 300"
        price = discount_price.text.strip()
    else:
        normal_price = game_item.select_one(".search_price")
        if normal_price:
            price = normal_price.text.strip()

    return {"name": name, "current_price": price}
