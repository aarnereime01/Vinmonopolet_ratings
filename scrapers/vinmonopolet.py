import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time

class Vinmonopolet:
    
    def __init__(self, product_type: str = 'rødvin', country: str = None, variety: str = None):
        self.product_type = product_type.lower()
        self.country = country.lower() if country is not None else None
        self.variety = variety.lower() if variety is not None else None
        
        self.max_pages = float('inf')
        self.data = {}
        
        self.base_url = 'https://www.vinmonopolet.no'
        self.url = f'https://www.vinmonopolet.no/search?searchType=product&q=%3Arelevance%3AmainCategory%3A{self.product_type}'
        
    def get_wines(self):
        # set up the driver path
        base_dir = os.path.join(os.path.dirname( __file__ ), '..' )
        chrome_driver_path = os.path.join(base_dir, 'chromedriver')
        
        # set up the driver
        service = Service(executable_path=chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = webdriver.Chrome(service=service, options=options)
        
        page = 0
        # retrieve elements from the page
        try:
            while page < self.max_pages:
                
                driver.get(self.url)
                html = driver.page_source
                soup = bs(html, 'html.parser')
                
                if page == 0:
                    # get the max number of pages
                    self.max_pages = int(soup.find('span', {'class': 'pagination-text'}).text.split()[-1])
                    print(self.max_pages)
                    
                # get all the wines on the page
                wines = soup.find_all('li', {'class': 'product-item'})
                for wine in wines:
                    
                    # get the link to the wine
                    link = wine.find('a', {'class': 'link-text button'})['href']
                    print(link)
                    
                    # get the name of the wine
                    name = wine.find('div', {'class': 'product__name'}).text
                    print(name)
                    
                    # get the district of the wine
                    district = wine.find('div', {'class': 'product__district'}).text
                    print(district)
                    
                    # get the price of the wine
                    price = wine.find('span', {'class': 'product__price'}).text
                    print(price)
                    
                    # get the volume of the wine
                    volume = wine.find('span', {'class': 'amount'}).text
                    print(volume)
                    
                    # get the availability of the wine
                    availability = wine.find_all('div', {'class': 'product-stock-status-line-text'})
                    stock = availability[0].span.text
                    delivery = availability[1].text
                    print(stock)
                    print(delivery)
                    break
                
                # go to next page
                
                time.sleep(5)
                
        
        except Exception as e:
            print(e)
            
        # update the url to include the max pages
        
        
        driver.quit()
        
    def format_wines(self):
        pass
        
        
if __name__ == '__main__':
    vinmonopolet = Vinmonopolet('rødvin')
    vinmonopolet.get_wines()