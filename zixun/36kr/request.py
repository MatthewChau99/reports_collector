import requests
from bs4 import BeautifulSoup
import time
import json

url = 'https://gateway.36kr.com/api/mis/nav/search/resultbytype'
payload = {"partner_id":"web","timestamp":1597836514683,"param":{"searchType":"article","searchWord":"中芯国际","sort":"score","pageSize":40,"pageEvent":0,"pageCallback":"eyJmaXJzdElkIjoxOCwibGFzdElkIjoxMywiZmlyc3RDcmVhdGVUaW1lIjozMDU0MiwibGFzdENyZWF0ZVRpbWUiOjM5NjI1NX0","siteId":1,"platformId":2}}
headers = {
    'accept':'*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'content-length': '293',
    'content-type': 'application/json',
    'cookie': 'Hm_lvt_1684191ccae0314c6254306a8333d090=1596210296; Hm_lvt_713123c60a0e86982326bae1a51083e1=1596210297; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22173a58c3e5e469-02e84f5fa3b948-3323765-2073600-173a58c3e5fa9a%22%2C%22%24device_id%22%3A%22173a58c3e5e469-02e84f5fa3b948-3323765-2073600-173a58c3e5fa9a%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; _ss_pp_id=d59787798bd08f8853d1596224723372; _td=2dab35d3-7b8a-48bc-bd03-96124935a411; acw_tc=2760827e15978348728514947ed067e1ffc7190f2e025127214afcfc370af8; Hm_lpvt_713123c60a0e86982326bae1a51083e1=1597836508; Hm_lpvt_1684191ccae0314c6254306a8333d090=1597836508',
    'origin': 'https://36kr.com',
    'referer': 'https://36kr.com/search/articles/%E4%B8%AD%E8%8A%AF%E5%9B%BD%E9%99%85?sort=score',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
res = requests.post(url, headers = headers, data = json.dumps(payload))
sum = open("summary"+".txt", "w", encoding='utf-8')

html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')
articles = res.json()
articles = articles['data']['itemList']
for obj in articles:
    print(obj['itemId'])
