import time
from bs4 import BeautifulSoup as BtS
import requests
from requests_html import HTMLSession
from datas import xheaders
from datas import headers_postauth
from itemclass import CsItem

TRIES_TO_PARSE = 25
TIME_PER_ONE_TRY = 5
VPN_ISO_CODE = "BY"


def getdict():
    for mlist in range(1, 11):
        url = f"https://buff.163.com/api/market/goods?game=csgo&page_num={mlist}&use_suggestion=0&_=1672932038531"
        wss = HTMLSession()
        loginresponse = wss.post(url='https://buff.163.com/account/api/user/info?_=1673003802570',
                                 headers=headers_postauth)
        if not(str(loginresponse) == '<Response [200]>'):
            print("Login error. Check Cokkies in datas.py/headers_postauth\n")
            exit()
        marketresponse = wss.get(url, headers=xheaders).json()
        yield marketresponse


page = 0
for i in getdict():
    counter = 0
    failpars = 0

    steamOrdersTotal = -1
    steamSellsTotal = -1
    steamMaxOrder = -1
    steamMinPrice = -1

    items = i['data']['items']
    for cit in items:
        itemurl = cit['steam_market_url']
        response = requests.get(itemurl, headers=xheaders)
        soup = BtS(response.text, "lxml")
        data = soup.find_all("script", type="text/javascript")
        ndata = str(data[-1].text)
        index = ndata.find("Market_LoadOrderSpread")
        _ids = ndata[index:index + 35]
        ids = _ids.split(' ')
        parsedscs = True
        if ids == ['']:
            parsedscs = False
            for try_parse in range(TRIES_TO_PARSE):
                print(f"error while parsing {cit['market_hash_name']}.\n"
                      f"Trying again ({try_parse})...\n")
                time.sleep(TIME_PER_ONE_TRY)
                response = requests.get(itemurl, headers=xheaders)
                soup = BtS(response.text, "lxml")
                data = soup.find_all("script", type="text/javascript")
                ndata = str(data[-1].text)
                index = ndata.find("Market_LoadOrderSpread")
                _ids = ndata[index:index + 35]
                ids = _ids.split(' ')
                if not(ids == ['']):
                    print(f"tried to parse, successful (it try no. {try_parse})\n")
                    parsedscs = True
                    break

        if parsedscs:
            itmid = ids[1]
            scriptUrl = f"https://steamcommunity.com/market/itemordershistogram?country={VPN_ISO_CODE}"
            scriptUrl += f"&language=russian&currency=1"
            scriptUrl += f"&item_nameid={itmid}&two_factor=0"
            scpriceSession = HTMLSession()
            steamPriceResponse = scpriceSession.get(scriptUrl, headers=xheaders).json()

            if not(steamPriceResponse is None):
                steamMinPrice = steamPriceResponse['lowest_sell_order']
                steamMaxOrder = steamPriceResponse['highest_buy_order']

                steamMinPrice = steamMinPrice[:-2] + '.' + steamMinPrice[-2:]
                steamMaxOrder = steamMaxOrder[:-2] + '.' + steamMaxOrder[-2:]

                steamOrdersTotal = steamPriceResponse['buy_order_graph'][0][1]

                _steamSellsTotal = str(steamPriceResponse['sell_order_summary'])
                startIndexSellsTotal = _steamSellsTotal.find('orders_header_promote">')
                endIndexSellsTotal = _steamSellsTotal.find('</span><br>')
                steamSellsTotal = _steamSellsTotal[startIndexSellsTotal+23:endIndexSellsTotal]

            else:
                for try_resp in range(TRIES_TO_PARSE):
                    print(f"None, so trying to get response again ({try_resp})...")
                    time.sleep(TIME_PER_ONE_TRY)
                    steamPriceResponse = scpriceSession.get(scriptUrl, headers=xheaders).json()
                    if not(steamPriceResponse is None):
                        print("Steam responsed not null.")
                        steamMinPrice = steamPriceResponse['lowest_sell_order']
                        steamMaxOrder = steamPriceResponse['highest_buy_order']

                        steamMinPrice = steamMinPrice[:-2] + '.' + steamMinPrice[-2:]
                        steamMaxOrder = steamMaxOrder[:-2] + '.' + steamMaxOrder[-2:]

                        steamOrdersTotal = steamPriceResponse['buy_order_graph'][0][1]

                        _steamSellsTotal = str(steamPriceResponse['sell_order_summary'])
                        startIndexSellsTotal = _steamSellsTotal.find('orders_header_promote">')
                        endIndexSellsTotal = _steamSellsTotal.find('</span><br>')
                        steamSellsTotal = _steamSellsTotal[startIndexSellsTotal + 23:endIndexSellsTotal]

            newitem = CsItem(
                cit['sell_min_price'],
                steamMinPrice,
                cit['buy_max_price'],
                steamMaxOrder,
                cit['goods_info']['icon_url'],
                cit['market_hash_name'],
                cit['sell_num'],
                cit['buy_num'],
                steamSellsTotal,
                steamOrdersTotal,
                cit['id'],
                cit['steam_market_url']
            )
            print(f"\nPARSED: {counter}\n")
            counter += 1
            newitem.printitem()
        else:
            print(f"Error while parsing item {cit['market_hash_name']}. Skipping...\n")
            failpars += 1
            time.sleep(30)
    print(f"Parsed page {page} with {failpars} failed items of 20\n\n\n")
    time.sleep(15)
    page += 1
