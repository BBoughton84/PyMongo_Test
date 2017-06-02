import requests
import os
import glob
import time

tempHolder = 99
# barcode = 810815021370
# barcode = '014113912839'
brandname = "Chaquita"
itemname = "Banana"
quantity = 3
item_id = "593060f70a857571dd39b7b0"


dataToSend = {"brand_name":brandname, "item_name":itemname, "quantity":quantity, "item_id":item_id}
source = requests.post('http://0.0.0.0:5000/insertman', data=dataToSend)
print(source.text)
print(source.status_code)
