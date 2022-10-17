# Web Scraping / Parsing / Hooking --> Internetdab ma'lumot yig'ish
# requests --> so'rovlar yuborish uchun
# BeautifulSoup4 --> HTML dan ma'lumot qidirishda ishlatiladi

'''
====================================================
try:
    print( 2 + "3" )  # TypeError
except Exception as exp:
    print( f"{exp.__class__.__name__}: {exp}" )

a = 17
if a <= 18:
    raise ValueError("Voyaga yetmagansiz!")
====================================================
'''

# http --> Hyper Text Transfer Protocol
# https --> Hyper Text Transfer Protocol Security

import requests
import json
from bs4 import BeautifulSoup

URL = "https://texnomart.uz/kr/katalog/noutbuki-apple-macbook"
HEADERS = {
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

def get_response(url: str, headers: dict) -> requests.Response | None:
    '''
    Return response from an url or None object if any error occurs
    '''
    response = requests.get(url=url, headers=headers)
    try:
        response.raise_for_status()
        return response
    except requests.HTTPError:
        print( f"Xatolik yuz berdi, status kod: {response.status_code}" )
        return None


def get_data(response: requests.Response) -> None:
    '''
    Gets a data from a response and writes it to a json file
    '''
    if response is not None:
        html = response.text
        soup = BeautifulSoup(markup=html, features="html.parser")
        
        wrapper = soup.find(name="div", attrs={"class": "products-box"})
        products = wrapper.find_all(name="div", attrs={"class": "col-3"}) # [<div>...</div>, <div>...</div>]
        
        for product in products:
            title = product.find(name="a", attrs={"class": "product-name"}).text.strip()
            price = product.find(name="div", class_="product-bottom__right").find_all("div")[1].text.strip()
            price_installment = product.find(name="div", class_="product-bottom__right").find_all("div")[2].text.replace("Муддатли тўлов", "").strip()
            link = "https://texnomart.uz/" + product.find(name="a", attrs={"class": "product-name"}).get("href")
            data = {}
            data["Maxsulot nomi"] = title
            data["Maxsulot narxi"] = price
            data["Maxsulot narxi*"] = price_installment
            data["Maxsulot sahifasi"] = link
            
            with open(file="apple_computers.json", mode="a", encoding="utf-8") as file:
                json.dump( obj=data, fp=file, indent=4, ensure_ascii=False )

get_data(response=get_response(url=URL, headers=HEADERS))

    



   









 





