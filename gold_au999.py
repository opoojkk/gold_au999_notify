import requests
from bs4 import BeautifulSoup

def fetch_gold_price(url="https://example.com", code="Au9999"):
    resp = requests.get(url)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.find_all("tr")
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if cols and cols[0].startswith(code):
            record = {
                "代码": cols[0],
                "名称": cols[1],
                "最新价": cols[2],
                "买入价": cols[3],
                "卖出价": cols[4],
                "涨跌额": cols[5],
                "涨跌幅": cols[6],
                "开盘价": cols[7],
                "最高价": cols[8],
                "最低价": cols[9],
                "昨收价": cols[10],
                "更新时间": cols[11],
                "单位": cols[12],
            }
            return record
    return None


if __name__ == "__main__":
    url = "https://example.com"   # ⚠️ 换成实际网址
    data = fetch_gold_price(url)
    if data:
        print("抓取成功：")
        for k, v in data.items():
            print(f"{k}: {v}")
    else:
        print("未找到 Au9999 数据")
