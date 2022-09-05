from binance.client import Client

import key


def likidasyon_hesapla(fiyat, kaldirac):
    geri_cekilme = 100 / kaldirac
    geri_cekilme = geri_cekilme * 0.5
    return fiyat - (fiyat * geri_cekilme / 100)


def ortalama_fiyat_hesapla(fiyat_bir, fiyat_iki, mal_bir, mal_iki):
    temp = (fiyat_bir * mal_bir + fiyat_iki * mal_iki) / (mal_bir + mal_iki)
    return round(temp, 4)


def pozisyon(fiyat, miktar):
    return [fiyat, miktar]


def miktat_topla(liste):
    temp = 0
    for i in liste:
        temp += i[1]
    return temp


# print(likidasyon_hesapla(250,50))


client = Client(api_key=key.pkey, api_secret=key.skey)
# coin_name = input("COİN NAME: ")
# quantity = input("Quantity: ")
# price = input("Price: ")
# kaldirac = input("Kaldıraç X: ")
#
coin_name = "BTC"
quantity = 0.001
price = 23860
kaldirac = 100

pozisyon_listesi = [[0, 0]]
# mal toplama
# client.futures_create_order(
#     symbol=coin_name + 'USDT',
#     positionSide="LONG",
#     side='BUY',
#     type=Client.FUTURE_ORDER_TYPE_LIMIT,
#     timeInForce='GTC',
#     quantity=quantity,
#     price=round(price,4),
#
# )
#
# pozisyon_listesi.append(pozisyon(price, quantity))
#
# print("----------")
# print("limit fiyat: " + str(price))
# print("miktar: " + str(quantity))
# print("----------")
#
# for i in range(3):
#     quantity = round((miktat_topla(pozisyon_listesi) * 2),2)
#     price = round(likidasyon_hesapla(
#         ortalama_fiyat_hesapla(pozisyon_listesi[i][0], pozisyon_listesi[i + 1][0], pozisyon_listesi[i][1],
#                                pozisyon_listesi[i + 1][1]), kaldirac),4)
#     print("----------")
#     print("limit fiyat: " + str(price))
#     print("miktar: " + str(quantity))
#     print("----------")
#
#     client.futures_create_order(
#         symbol=coin_name + 'USDT',
#         positionSide="LONG",
#         side='BUY',
#         type=Client.FUTURE_ORDER_TYPE_LIMIT,
#         timeInForce='GTC',
#         quantity=quantity,
#         price=round(price,4),
#
#     )
#     pozisyon_listesi.append(pozisyon(price,quantity))

# /-********************************************************************************************
# hedge al sat
# coin_name ="CHZ"
# quantity = 545
# price = round(float(client.get_margin_price_index(symbol='CHZUSDT')["price"]),5)
#
#
# client.futures_create_order(
#     symbol=coin_name + 'USDT',
#     positionSide="SHORT",
#     side='SELL',
#     type=Client.ORDER_TYPE_MARKET,
#     # timeInForce='GTC',
#     quantity=quantity,
#     # price=round(price,4),
# )
#
# # LİKİDASYON ENGELLME
# client.futures_create_order(
#     symbol=coin_name + 'USDT',
#     positionSide="SHORT",
#     side='BUY',
#     type=Client.FUTURE_ORDER_TYPE_STOP,
#     timeInForce='GTC',
#     quantity=quantity,
#     stopPrice=round(price+price*0.007,5),
#     price=round(price+price*0.0075,5),
# )
#
#
# # KAAR OLANI KAPATMA
# client.futures_create_order(
#     symbol=coin_name + 'USDT',
#     positionSide="SHORT",
#     side='BUY',
#     type=Client.FUTURE_ORDER_TYPE_LIMIT,
#     timeInForce='GTC',
#     quantity=quantity,
#     price=round(price-price*0.0060,5),
# )
# # 0,05
#
#
#
# # LONG POZİSYONU
# client.futures_create_order(
#     symbol=coin_name + 'USDT',
#     positionSide="LONG",
#     side='BUY',
#     type=Client.ORDER_TYPE_MARKET,
#     # timeInForce='GTC',
#     quantity=quantity,
#     # price=round(price,4),
# )
#
# # LİKİDASYON ENGELLME
# client.futures_create_order(
#     symbol=coin_name + 'USDT',
#     positionSide="LONG",
#     side='SELL',
#     type=Client.FUTURE_ORDER_TYPE_STOP,
#     timeInForce='GTC',
#     quantity=quantity,
#     stopPrice=round(price-price*0.007,5),
#     price=round(price-price*0.0075,5),
# )
#
#
# # KAAR OLANI KAPATMA
# client.futures_create_order(
#     symbol=coin_name + 'USDT',
#     positionSide="LONG",
#     side='SELL',
#     type=Client.FUTURE_ORDER_TYPE_LIMIT,
#     timeInForce='GTC',
#     quantity=quantity,
#     price=round(price+price*0.0060,5),
# )


# **********************************************************

# ARAYÜZ BACKEND
virgul_sonrası = 3

carpan = 2

def ondalık_belirleme(price):
    temp = str(price)
    return len(temp[temp.find("."):]) - 1


def pozisyon_belirleme(coin_name,price,quantity,long_or_short):
    # virgül sornası belirleme
    global virgul_sonrası
    virgul_sonrası = ondalık_belirleme(price)

    if(long_or_short == "LONG"):
        long_pozisyonu(coin_name, price, quantity)


    elif(long_or_short == "SHORT"):
        short_pozisyonu(coin_name, price, quantity)


def izsüren_belirleme(coin_name,price,quantity,long_or_short,oran):
    if(long_or_short == "LONG"):
        # print("long")
        izsüren_stop_long(coin_name,price,quantity,oran)



    elif(long_or_short == "SHORT"):
        # print("short")
        izsüren_stop_short(coin_name, price, quantity, oran)



def izsüren_stop_long(coin_name,price,quantity,oran):
    global carpan
    stop_fiyat = price + price * 0.0001*oran*carpan
    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="LONG",
        side='SELL',
        type=Client.FUTURE_ORDER_TYPE_STOP,
        timeInForce='GTC',
        quantity=quantity,
        stopPrice=round(stop_fiyat, virgul_sonrası),
        price=round(stop_fiyat - stop_fiyat*0.0005, virgul_sonrası),
    )


def izsüren_stop_short(coin_name,price,quantity,oran):
    global carpan
    stop_fiyat = price - price * 0.0001*oran*carpan
    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="SHORT",
        side='BUY',
        type=Client.FUTURE_ORDER_TYPE_STOP,
        timeInForce='GTC',
        quantity=quantity,
        stopPrice=round(stop_fiyat, virgul_sonrası),
        price=round(stop_fiyat + stop_fiyat*0.0005, virgul_sonrası),
    )




def long_pozisyonu(coin_name,price,quantity):
    global carpan

    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="LONG",
        side='BUY',
        type=Client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce='GTC',
        quantity=quantity,
        price=round(price, virgul_sonrası),
    )

    # zarar kes
    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="LONG",
        side='SELL',
        type=Client.FUTURE_ORDER_TYPE_STOP,
        timeInForce='GTC',
        quantity=quantity,
        stopPrice=round(price - price * 0.0018*carpan, virgul_sonrası),
        price=round(price - price * 0.0020*carpan, virgul_sonrası),
    )

    # kar al
    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="LONG",
        side='SELL',
        type=Client.FUTURE_ORDER_TYPE_STOP,
        timeInForce='GTC',
        quantity=quantity,
        stopPrice=round(price, virgul_sonrası),
        price=round(price + price * 0.005*carpan, virgul_sonrası),
    )





# ----------------------------------------------------------------------------------------




def short_pozisyonu(coin_name,price,quantity):
    global carpan
    # pozisyon short
    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="SHORT",
        side='SELL',
        type=Client.FUTURE_ORDER_TYPE_LIMIT,
        timeInForce='GTC',
        quantity=quantity,
        price=round(price, virgul_sonrası),
    )

    # zarar kes
    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="SHORT",
        side='BUY',
        type=Client.FUTURE_ORDER_TYPE_STOP,
        timeInForce='GTC',
        quantity=quantity,
        stopPrice=round(price + price * 0.0018*carpan, virgul_sonrası),
        price=round(price + price * 0.0020*carpan, virgul_sonrası),
    )

    # kar al
    client.futures_create_order(
        symbol=coin_name + 'USDT',
        positionSide="SHORT",
        side='BUY',
        type=Client.FUTURE_ORDER_TYPE_STOP,
        timeInForce='GTC',
        quantity=quantity,
        stopPrice=round(price, virgul_sonrası),
        price=round(price - price * 0.005*carpan, virgul_sonrası),
    )
