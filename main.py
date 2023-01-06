from bs4 import BeautifulSoup as BtS
import requests
from requests_html import HTMLSession
from requests import Session
import lxml
from datas import xheaders
from itemclass import CsItem
import os

def getdict():
    for mlist in range(1, 11):
        url = f"https://buff.163.com/api/market/goods?game=csgo&page_num={mlist}&use_suggestion=0&_=1672932038531"
        wss = HTMLSession()
        headers_postauth = {
            "Accept": 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,ru-BY;q=0.8,ru;q=0.7',
            'Connection': 'keep-alive',
            'Cookie': 'Device-Id=byWUusQzPAjaL1gazq6J; P_INFO=375-297505821|1662832717|1|netease_buff|00&99|null&null&null#BY&null#10#0|&0||375-297505821; Locale-Supported=en; game=csgo; amp_932404=M6siBr_2D14aD4dG2rzHkG...1gm1rdgqo.1gm1ubges.0.0.0; session=1-uMtNDW6TdDd9DWJu13kzOlEll-tW1tKyRVVsygv9zNpF2034838659; csrf_token=IjdhNDI5YmNjMTFmOGU5YTI1NzE3NmM4MWY3NmI2MzgyYmMwNWNiZmIi.FpjWnw.uPDbjmKW-8nqodXGGQq8wwnDggk',
            'Host': 'buff.163.com',
            'Referer': r'https://buff.163.com/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': 'Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': 'Windows'
        }
        wss.post(url='https://buff.163.com/account/api/user/info?_=1672955149985', headers=headers_postauth)
        marketresponse = wss.get(url, headers=xheaders).json()
        yield marketresponse


for i in getdict():
    print(i)
    items = i['data']['items']
    print(items)
    print('\n')
    for cit in items:
        itemurl = cit['steam_market_url']
        response = requests.get(itemurl, headers=xheaders)
        # Market_LoadOrderSpread
        soup = BtS(response.text, "lxml")
        data = soup.find_all("script", type="text/javascript")
        ndata = str(data[-1].text)
        index = ndata.find("Market_LoadOrderSpread")
        _ids = ndata[index:index+35]
        ids = _ids.split(' ')
        itmid = ids[1]
        scriptUrl = f"https://steamcommunity.com/market/itemordershistogram?country=" \
                    f"BY&language=russian&currency=1&item_nameid={itmid}&two_factor=0"
        scpriceSession = HTMLSession()
        steamPriceResponse = scpriceSession.get(scriptUrl, headers=xheaders).json()

        if not(steamPriceResponse is None):
            steamMinPrice = steamPriceResponse['lowest_sell_order']
            steamMaxOrder = steamPriceResponse['highest_buy_order']

            steamMinPrice = steamMinPrice[:-2] + '.' + steamMinPrice[-2:]
            steamMaxOrder = steamMaxOrder[:-2] + '.' + steamMaxOrder[-2:]

        else:
            steamMinPrice = -1
            steamMaxOrder = -1
            steamOrdersTotal = -1

        newitem = CsItem(
            cit['sell_min_price'],
            steamMinPrice,
            cit['buy_max_price'],
            steamMaxOrder,
            cit['goods_info']['icon_url'],
            cit['market_hash_name'],
            cit['sell_num'],
            cit['buy_num'],
            -1,
            -1,
            cit['id'],
            cit['steam_market_url']
        )


# GET /account/api/user/info?_=1672955149985 HTTP/1.1
# Accept: application/json, text/javascript, */*; q=0.01
# Accept-Encoding: gzip, deflate, br
# Accept-Language: en-US,en;q=0.9,ru-BY;q=0.8,ru;q=0.7
# Connection: keep-alive
# Cookie: Device-Id=byWUusQzPAjaL1gazq6J; P_INFO=375-297505821|1662832717|1|netease_buff|00&99|null&null&null#BY&null#10#0|&0||375-297505821; Locale-Supported=en; game=csgo; amp_932404=M6siBr_2D14aD4dG2rzHkG...1gm1rdgqo.1gm1ubges.0.0.0; session=1-uMtNDW6TdDd9DWJu13kzOlEll-tW1tKyRVVsygv9zNpF2034838659; csrf_token=IjdhNDI5YmNjMTFmOGU5YTI1NzE3NmM4MWY3NmI2MzgyYmMwNWNiZmIi.FpjWnw.uPDbjmKW-8nqodXGGQq8wwnDggk
# Host: buff.163.com
# Referer: https://buff.163.com/
# Sec-Fetch-Dest: empty
# Sec-Fetch-Mode: cors
# Sec-Fetch-Site: same-origin
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36
# X-Requested-With: XMLHttpRequest
# sec-ch-ua: "Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"
# sec-ch-ua-mobile: ?0
# sec-ch-ua-platform: "Windows"
