import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

laptop_dict = {
    'name': [],
    'price': [],
    'shipping': [],
    'link': []
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
session = requests.Session()
with open("cookies.json", "r", encoding="utf-8") as f:
    cookie_json = json.load(f)

cookies = {cookie['name']: cookie['value'] for cookie in cookie_json}

page_num=1
while True:
    url=f"https://www.ebay.com/sch/i.html?_dcat=177&_fsrp=1&_from=R40&RAM%2520Size=32%2520GB&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&_pgn={page_num}&rt=nc"
    #url=f"https://www.ebay.com/sch/i.html?_fsrp=1&_from=R40&_nkw=laptop&_sacat=0&SSD%2520Capacity=1%2520TB&rt=nc&RAM%2520Size=16%2520GB%7C32%2520GB%7C8%2520GB&_dcat=177&_pgn={page_num}"
    response=requests.get(url,headers=headers,cookies=cookies)
    print(f"{page_num}. page scraped")
    if response.status_code != 200:
        continue
    soup=BeautifulSoup(response.text, "html.parser")
    container = soup.find('div', attrs={'id': 'srp-river-results'})
    laptops = container.find_all('div', class_='s-item__info')
    current_page_names = []  # Bu səhifədəki adlar
    for laptop in laptops:
        if laptop.find('span',attrs={'role':'heading'}).text is not None:
            name=laptop.find('span',attrs={'role':'heading'}).text
        else:
            print('Melumat Yoxdur')
        laptop_dict['name'].append(name)
        current_page_names.append(name.strip())

        if laptop.find('span',class_='s-item__price').text is not None:
            price=laptop.find('span',class_='s-item__price').text
        else:
            print("Melumat yoxdur")
        laptop_dict['price'].append(price)

        if laptop.find('span',class_='s-item__shipping s-item__logisticsCost').text is not None:
            shipping=laptop.find('span',class_='s-item__shipping s-item__logisticsCost').text
        else:
            print("Melumat yoxdur")
        laptop_dict['shipping'].append(shipping)


        if laptop.find('a',class_='s-item__link')['href'] is not None:
            link=laptop.find('a',class_='s-item__link')['href']
        else:
            print("Melumat yoxdur")
        laptop_dict['link'].append(link)
    
    
        
    next_butonu=soup.find('button',class_='pagination__next')
    if next_butonu is not None:
        break
    page_num+=1
    df=pd.DataFrame(laptop_dict)


    df.index = df.index + 1  # İndeksi 1-dən başlat
    df.to_csv("laptops.csv", index=True, index_label="", quoting=1)



