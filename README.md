# BUFF163 (BUFF.MARKET in future) <-> steamcommunity prices sorter in TG BOT

## CURRENT VERSION: 0.1 -> 0.1.X

Version control

0.1:
  
  >Can parse every page on buff.163.com (name, img url; price, order price, items amount, orders amount, and the same for steam) and create CsItem-type objects with datas - done
  
      0.1.1:
      
      Added url-croppers
      prepared system to tor-mode
      created pre-xlsx system
      
      0.1.2:
      
      Finished xlsx-writer system
  
0.2:

  >Can write all CsItems from Project to DB (.csv or .xlsx) and compare server data with DB
  
0.3:

  >Can sort items by steam price, buff price, buff-steam (%), items amount
  
0.4:

  >Filter items (by price, amount, orders, orders amount)
  
0.5:

  >Update parse data (+rarity, wear (exterior), type, category)
  
0.6:

  >Create Telegram bot:
  
    0.6.1:
  
      Bot can print first page of items (one item in one message)
    
    0.6.2:
  
      Bot can sort all pages by (...) and print 25 items by clicking each other
    
     0.6.3:
   
      Bot can filter items by (...) and print them
    
    0.6.4:
    
      Other bot features (in the future)
      
0.7:
      
      Auth in bot (By key XXXX-XXXX-XXXX-XXXX)
      Other system changes (in the future)
  
# 1.0:
      Telegram bot can sort items by (%) in steam<->buff markets to buy items, filter them and etc
  
# 2.0:
      All from 1.0, but with BUFF.MARKET market


## TODO

Current version (0.1):
  > CsItem to db writer
  > 
  > If item already in db, re-write prices and orders
  > 
  > If -1 value, do not write and break
  > 
  > import from db
  >
  > Or skip item if already in DB
  >
  > Proxy (dynamic-ip) request system
  

