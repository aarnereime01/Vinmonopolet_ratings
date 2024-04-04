import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import time
import datetime
import random

class Vinmonopolet:
    
    def __init__(self, product_type: str = 'rødvin'):
        self.product_type = product_type.lower()
        
        self.base_dir = os.path.join(os.path.dirname( __file__ ), '..' )
        self.chrome_driver_path = os.path.join(self.base_dir, 'chromedriver')
        
        self.max_pages = float('inf')
        self.data = {}
        
        self.base_url = 'https://www.vinmonopolet.no'
        self.url = f'https://www.vinmonopolet.no/search?searchType=product&q=%3Arelevance%3AmainCategory%3A{self.product_type}'
        
        self.dataframe = self.make_dataframe()
        
    def get_wines(self):
        # set up the driver
        service = Service(executable_path=self.chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        page = 0
        # retrieve elements from the page
        try:
            while page <= self.max_pages:
                start_time = time.time()
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(self.url)
                time.sleep(random.randint(1,3))
                html = driver.page_source
                soup = bs(html, 'html.parser')
                
                if page == 0:
                    # get the max number of pages
                    self.max_pages = int(soup.find('span', {'class': 'pagination-text'}).text.split()[-1])
                   
                # get all the wines on the page
                wines = soup.find_all('li', {'class': 'product-item'})
                
                # lne_wines = len(wines)
                # if lne_wines != 24:
                #     print(f'Found {len(wines)} wines on page {page}')
                
                for wine in wines:
                    # get the link to the wine
                    link = wine.find('a', {'class': 'link-text button'})['href']
                    
                    # get product code
                    product_code = int(wine.find('div', {'class': 'product__code'}).text)
                    
                    # get the name of the wine
                    name = wine.find('div', {'class': 'product__name'}).text
                    
                    # get the district of the wine
                    district = wine.find('div', {'class': 'product__district'}).text
                    
                    # get the price of the wine
                    price = wine.find('span', {'class': 'product__price'}).text
                    
                    # get the volume of the wine
                    volume = wine.find('span', {'class': 'amount'}).text
                    
                    # get the availability of the wine
                    availability = wine.find_all('div', {'class': 'product-stock-status-line-text'})
                    stock = availability[0].span.text
                    delivery = availability[1].text
                    
                    # format the data
                    product_name, year = self.format_product_name(name)
                    link = self.format_link(link)
                    country, district, subdistrict = self.format_district(district)
                    price = self.format_price(price)
                    volume = self.format_volume(volume)
                    stock = self.format_stock(stock)
                    delivery = self.format_delivery(delivery)
                    
                    # format the data
                    self.data[product_code] = {
                        'product_name': product_name,
                        'year': year,
                        'link': link,
                        'country': country,
                        'district': district,
                        'subdistrict': subdistrict,
                        'price': price,
                        'volume': volume,
                        'stock': stock,
                        'delivery': delivery
                    }
                    
                end_time = time.time()
                
                # update the url to get the next page
                page += 1
                print(f'Page {page} of {self.max_pages} done')
                self.url = f'https://www.vinmonopolet.no/search?searchType=product&currentPage={page}&q=%3Arelevance%3AmainCategory%3A{self.product_type}'        
                if page == 1:
                    duration = (end_time - start_time) * self.max_pages
                    time_to_complete = datetime.datetime.now() + datetime.timedelta(seconds=duration)
                    print(f'Scraping will be done approximately at {time_to_complete}')
                    
                driver.quit()
                
        except Exception as e:
            print(e)
        
        driver.quit()
        
    def format_link(self, link: str):
        return self.base_url + link
        
    def format_product_name(self, name: str):
        name = name.split()
        year = int(name[-1]) if name[-1].isnumeric() else None
        product_name = ' '.join(name[:-1]) if year is not None else ' '.join(name)
        return product_name, year
    
    def format_district(self, district: str):
        areas = district.split(', ')
        country = areas[0]
        district = areas[1] if len(areas) > 1 else None
        subdistrict = areas[2] if len(areas) > 2 else None
        return country, district, subdistrict
    
    def format_price(self, price: str):
        price = price.replace('Kr', '').replace(',', '.').split()
        price = ''.join(price)
        return float(price)
    
    def format_volume(self, volume: str):
        volume = volume.split()[0].replace(',', '.')
        return float(volume)
    
    def format_stock(self, stock: str):
        # will come back to this
        return stock
    
    def format_delivery(self, delivery: str):
        # will come back to this
        return delivery
    
    def make_dataframe(self):
        self.get_wines()
        df = pd.DataFrame.from_dict(self.data, orient='index')
        
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'product_code'}, inplace=True)
        df.to_excel(f'{self.base_dir}/datasets/{self.product_type}_vinmonopolet.xlsx', index=False)
        return df
        
        
if __name__ == '__main__':
    vinmonopolet = Vinmonopolet('rødvin')
    print(len(vinmonopolet.dataframe))