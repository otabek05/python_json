

import requests
import json
from bs4 import BeautifulSoup

URL = "https://texnomart.uz/kr/katalog/vse-televizory"
HEADERS = {
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}
def get_response(url:str ,headers:dict) ->requests.Response:
    response=requests.get(url=URL,headers=HEADERS)
    try:
        response.raise_for_status()
        return response
    except requests.HTTPError:
        print(f'Something went wrong! status code: {response.status_code}')
        return None
def malumotlar_olish(response:requests.Response) -> None:
    if response is not None:
        html=response.text
        soup=BeautifulSoup(markup=html, features="html.parser")
        s_wrapper = soup.find("div", class_="o-hidden")
        products=s_wrapper.find_all("div", class_="col-3")
        data={}
        for product in products:
            title=product.find('a', class_="product-name").text.strip()
            price=product.find("div", class_="f-16").text.strip()
            installment_price=product.find("div", class_="installment-price").text.strip()
            link="https://texnomart.uz"+product.find("a", class_="product-name").get('href')

            data['title']=title
            data['price']=price
            data['installment price']=installment_price
            data['link']=link
            with open(file="product.json",mode='a',encoding="utf-8") as file:
                json.dump( data, file, indent=3, ensure_ascii=False )

malumotlar_olish(response=get_response(url=URL, headers=HEADERS))


