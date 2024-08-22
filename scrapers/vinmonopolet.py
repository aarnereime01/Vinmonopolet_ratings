from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time
import random

import sys
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent))

import scraper
from common.config import load_config

# retrieve filters used to modify the url
# filters = load_config('vinmonopolet.yaml')

class Vinmonopolet(scraper.Scraper):
    
    def __init__(self, website_name: str):
        super().__init__(website_name)
        
        # define the base url and the url to scrape
        self.base_url = 'https://www.vinmonopolet.no'
        self.url = 'https://www.vinmonopolet.no/search?searchType=product&q=%3Aprice-desc%3Abuyable%3Atrue%3Aprice%3A500%3Aprice%3A750%3Aprice%3A1000%3Aprice%3A5000%3AvolumeRanges%3A75+-+99+cl'

        # define the max number of pages
        self.max_pages = float('inf')
        
    def get_wines(self):
        page_num = 0
        # retrieve elements from the page
        try:
            # while page_num <= self.max_pages:
            while page_num <= 2:
                
                start_time = time.time()
                
                driver = webdriver.Chrome(options=self.options)
                driver.get(self.url)
                
                time.sleep(random.randint(1,3))
                
                html = driver.page_source
                soup = bs(html, 'html.parser')
                
                # scrape the page
                self.perform_scrape(soup, page_num)
                    
                end_time = time.time()
                
                # update the url to get the next page
                page_num += 1
                print(f'Page {page_num} of {self.max_pages} done')
                self.url = f'https://www.vinmonopolet.no/search?searchType=product&currentPage={page_num}&q=%3Aprice-desc%3Abuyable%3Atrue%3Aprice%3A500%3Aprice%3A750%3Aprice%3A1000%3Aprice%3A5000%3AvolumeRanges%3A75+-+99+cl'   
                if page_num == 1:
                    self.calculate_time_to_scrape(start_time, end_time, self.max_pages)
                    
                driver.quit()
                
        except Exception as e:
            print(e)
        
        driver.quit()
        
    def perform_scrape(self, soup: bs, page_num: int = 0):
            if page_num == 0:
                print('first page')
                # get the max number of pages
                self.max_pages = int(soup.find('span', {'class': 'pagination-text'}).text.split()[-1])
                print(self.max_pages)

            # get all the wines on the page
            wines = soup.find_all('li', {'class': 'product-item'})

            for wine in wines:
                # get the product category of the wine
                product_category = wine.find('div', {'class': 'product__category-name'}).text

                # skip the product if it is not a wine
                if product_category not in {'Rødvin', 'Hvitvin', 'Musserende vin'}:
                    continue
                
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
                stock = availability[0].div.text
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
                    'product_full_name': name,
                    'product_name': product_name,
                    'product_category': product_category,
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
        
if __name__ == '__main__':
    vinmonopolet = Vinmonopolet('vinmonopolet')
    vinmonopolet.get_wines()
    df = vinmonopolet.make_dataframe()