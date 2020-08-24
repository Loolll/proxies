import requests
from bs4 import BeautifulSoup as bs
from bs4 import element
import base64
import asyncio
import aiohttp
from aiohttp_proxy import ProxyConnector, ProxyType
CONCURRENCY = 20
TIMEOUT = 15


with open('proxies_hand', 'w') as file:
    pass
proxies = []
ips = []
content: str
with open('proxy.html', 'r', encoding='UTF-8') as file:
    content = file.read()
soup = bs(content, 'lxml')
for proxy_html in soup.find_all("tr"):
    proxy_td = proxy_html.find_all('td')
    try:
        pass_script: element.Tag = proxy_td[0].find('script', type="text/javascript")
        ip = str(proxy_td[0].text).lstrip(str(pass_script)).strip()
        port = proxy_td[1].find('span').text
        if ip not in ips:
            ips.append(ip)
            with open('proxies_hand', 'a') as file:
                proxy = str(ip) + ':' + str(port)
                file.write(proxy + '\n')
                proxies.append({'http': proxy, 'https': proxy})
    except IndexError:
        pass

with open('proxies_hand', 'a') as file:
    file.write('\n -------------------------------------------------- \n')


async def call_ulr(i, session, proxy):
    url = 'http://icanhazip.com/'
    try:
        print(f'Task {i}')
        async with session.get(url=url, proxy=('http://' + proxy['http'])) as response:
            with open('proxies_hand', 'a') as file:
                file.write(str(proxy) + '\n')
            print(proxy, response.text, '\n')
    except aiohttp.ClientProxyConnectionError:
        print(proxy, 'None', '\n')
    except aiohttp.ServerDisconnectedError:
        print(proxy, 'None', '\n')


async def main():
    for i, proxy in enumerate(proxies):
        async with aiohttp.ClientSession() as session:
            _ = await call_ulr(i, session, proxy)


ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(main())
