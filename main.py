import requests
from bs4 import BeautifulSoup as bs
from bs4 import element
import base64

with open('proxies', 'w') as file:
    pass
proxies = []
for i in range(10):
    response = requests.get(f'http://free-proxy.cz/ru/proxylist/country/RU/http/ping/all/{i}')
    content = response.text
    soup = bs(content, 'lxml')
    for proxy_html in soup.find_all("tr"):
        proxy_td = proxy_html.find_all('td')
        try:
            ip_in_script: element.Tag = proxy_td[0].find('script', type="text/javascript")
            ip_in_base64 = str(ip_in_script).split('"')[3]
            ip = str(base64.b64decode(ip_in_base64)).split("'")[1]
            port = proxy_td[1].find('span').text
            with open('proxies', 'a') as file:
                proxy = str(ip) + ':' + str(port)
                file.write(proxy + '\n')
                proxies.append({'http': proxy, 'https': proxy})
        except IndexError:
            pass

print(proxies)
with open('proxies', 'a') as file:
    file.write('\n -------------------------------------------------- \n')
for proxy in proxies:
    try:
        response = requests.get('http://icanhazip.com/', proxies=proxy)
        with open('proxies', 'a') as file:
            file.write(str(proxy) + '\n')
        print(proxy, response.text, '\n')
    except:
        print(proxy, 'None', '\n')
