import requests
import os
import glob
import time

tempHolder = 99

dataToSend = {"barcode":"848484", "temperature":tempHolder}
source = requests.post('http://0.0.0.0:5000/insert', data=dataToSend)
print(source.content)
print(source.status_code)
