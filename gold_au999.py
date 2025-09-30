import requests
from bs4 import BeautifulSoup

url = "https://quote.cngold.org/gjs/jjs.html"  # 换成真实的网页地址
resp = requests.get(url)
resp.encoding = "utf-8"

soup = BeautifulSoup(resp.text, "html.parser")

data_list = []

# 假设表格是 <table><tr><td>...</td></tr></table>
rows = soup.find_all("tr")
for row in rows:
    cols = [td.get_text(strip=True) for td in row.find_all("td")]
    if cols and cols[0].startswith("Au9999"):  # 找 Au9999 这一行
        # 映射到字段
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
        data_list.append(record)

print(data_list)
