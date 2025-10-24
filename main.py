from ping3 import ping
import requests  

#PING
try:
    delay = ping(input("Hostname: "), timeout=2)    #input меняем на значение элемента на сайте
    print('Ping успешен!')
except OSError as e:
    print('Ошибка '+e)

#geoip API
IPINFO_TOKEN = "50278a4342f406"
ip_address = '8.8.8.8'
url = f'https://ipinfo.io/{ip_address}'
headers = {'Authorization': f'Bearer {IPINFO_TOKEN}'}
response = requests.get(url, headers=headers)
print(response.text)  # Данные с API