# import requests
#
# headers = {
#     'Accept': 'application/json',
#     'Content-Type': 'application/json',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
#     'APItoken': 'e7d82-0913c-5fe10-603c2-be99e-a42e9-a837'
# }
#
#
# get_orders = requests.get('https://api.teapplix.com/api2/OrderNotification?DetailLevel=shipping|none|inventory|dropship&TxnId=RET-15-11229-21819', headers=headers).json()
# print(get_orders.get('Orders', '')[0])


print(dict)