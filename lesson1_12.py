import requests
import json
from bs4 import BeautifulSoup


URL = "https://texnomart.uz/kr/katalog/noutbuki"
HEADERS = {
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}

class BaseParser:
    def __init__(self, url, headers):
        self.url = url  
        self.headers = headers
    
    @staticmethod
    def get_response(url: str, headers: dict) -> requests.Response | None:
        response = requests.get(url=url, headers=headers)
        try:
            response.raise_for_status()
            return response
        except requests.HTTPError:
            print( f"Xatolik yuz berdi, status kod: {response.status_code}" )
            return None
    
    def get_data(self, url: str, headers: dict) -> None:
        response = self.get_response(url=self.url, headers=self.headers)
        if response is not None:
            html = response.text
            soup = BeautifulSoup(markup=html, features="html.parser")
            c_wrapper = soup.find("div", class_="category__wrap")
            categories = c_wrapper.find_all("div", class_="category__item")
            count = 0
            i = len(categories)
            for category in categories:
                count += 1
                c_title = category.find("h2", class_="content__title").text.strip()
                c_link = "https://texnomart.uz" + category.find("a", class_="category__link").get("href")
                
                response = self.get_response(url=c_link, headers=self.headers)
                if response is not None:
                    html = response.text
                    soup = BeautifulSoup(markup=html, features="html.parser")
                    p_wrapper = soup.find("div", class_="products-box")
                    products = p_wrapper.find_all("div", class_="col-3")
                    print( f"[INFO] {i}/{count} {c_title} ..." )
                    for product in products:
                        p_title = product.find("a", class_="product-name").text.strip()
                        p_link = "https://texnomart.uz" + product.find("a", class_="product-name").get("href")
                        p_price = product.find("div", class_="product-bottom__right").find_all("div")[1].text.strip()
                        p_price_installment = product.find("div", class_="installment-price").text.replace("Муддатли тўлов", "").strip()
                        
                        data = {}
                        data["Maxsulot nomi"] = p_title
                        data["Maxsulot sahifasi"] = p_link
                        data["Maxsulot narxi"] = p_price
                        data["Maxsulot narxi*"] = p_price_installment
                        # data["Maxsulot kategoriyasi"] = c_title
                        # data["Maxsulot kategoriyasi sahifasi"] = c_link
                        
                        with open(file=f"categories/{c_title}.json", mode="a", encoding="utf-8") as file:
                            json.dump( data, file, indent=3, ensure_ascii=False )
                        
                    
                
    
    def run(self):
        self.get_data(url=self.url, headers=self.headers)
    
    
    
    

parser = BaseParser(url=URL, headers=HEADERS)
parser.run()

    



