class CsItem:
    def __init__(
            self,
            buffminprice,
            steamminprice,
            buffmaxorder,
            steammaxorder,
            imgurl,
            csitname,
            buffamount,
            buffordersamount,
            steamamount,
            steamordersamount,
            itid,
            steam_url
                 ):
        self.buffprice = buffminprice       # Минимальная цена, за которую предмет выставили на buff163
        self.steamprice = steamminprice     # Минимальная цена, за которую предмет выставили на Steam
        self.bufforder = buffmaxorder       # Максимальная цена ордера на buff163
        self.steamorder = steammaxorder     # Максимальная цена ордера на steam
        self.imgurl = imgurl                # URL-адрес картинки скина
        self.name = csitname                # Полное имя скина
        self.buffamount = buffamount        # Кол-во предметов, выставленных на buff163
        self.buffordersamount = buffordersamount    # Кол-во ордеров, выставленных на предмет на buff163
        self.steamamount = steamamount       # Кол-во предметов, выставленных на steam
        self.steamordersamount = steamordersamount   # Кол-во ордеров, выставленных на предмет на steam
        self.id = itid                      # id предмета для получения ссылки goods
        self.steamurl = steam_url           # ссылка на предмет на steam

    def printitem(self):
        print(f"CSGO Item Printing...\n"
              f"Item name: {self.name}\n"
              f"BUFF163 Price: {self.buffprice}¥\n"
              f"BUFF163 Order: {self.bufforder}¥\n"
              f"Steam Price: {self.steamprice}$\n"
              f"Steam Order: {self.steamorder}$\n"
              f"Icon URL: https://g.fp.ps.netease.com/market/file/{self.imgurl}\n"
              f"Steam URL: https://steamcommunity.com/market/listings/730/{self.steamurl}\n"
              fr"Item url on buff: https://buff.163.com/goods/{self.id}?from=market#tab=selling"
              f"\nAmount (on BUFF163): {self.buffamount}\n"
              f"Amount (on Steam): {self.steamamount}\n"
              f"Order amount (on BUFF163): {self.buffordersamount}\n"
              f"Order amount (on Steam): {self.steamordersamount}\n")
        print('\n')
