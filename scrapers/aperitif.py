import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import time
import datetime

class Aperitif:
    
    def __init__(self, product_type: str = 'rødvin'):
        self.product_type = product_type.lower()
        
        self.base_dir = os.path.join(os.path.dirname( __file__ ), '..' )
        self.chrome_driver_path = os.path.join(self.base_dir, 'chromedriver')
        
        self.max_pages = float('inf')
        self.data = {}
        
        self.base_url = 'https://www.aperitif.no'
        self.url = f'https://www.aperitif.no/pollisten/pollisten-vin-{self.product_type},5?c[min]=&c[max]=&is_active=1&ordering=points_desc&query='
        
        self.dataframe = self.make_dataframe()
        
    def get_wines(self):
        # set up the driver
        service = Service(executable_path=self.chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        
        wines_skipped = 0
        page = 1
        # retrieve elements from the page
        try:
            while page <= self.max_pages:
                start_time = time.time()
                driver = webdriver.Chrome(service=service, options=options)
                driver.get(self.url)
                html = driver.page_source
                soup = bs(html, 'html.parser')
                
                if page == 1:
                    # get the max number of pages
                    max_page = soup.find('a', {'title': 'Siste'})['href'].split(',')[-1].split('?')[0]
                    self.max_pages = int(max_page)
                   
                # get all the wines on the page
                wines = soup.find_all('li', {'class': 'product-list-element'})
            
                for wine in wines:
                    # get product code
                    try:
                        product_code = int(wine.find('span', {'class': 'index'}).text[1:-1])
                    except:
                        wines_skipped += 1
                        continue

                                        
                    # get the name of the wine
                    name = wine.find('div', {'class': 'title'}).text.strip()
                    
                    # get the rating of the wine
                    try:
                        rating = int(wine.find('span', {'class': 'number'}).text)
                    except:
                        wines_skipped += 1
                        continue
                    # format the data
                    product_name, year = self.format_product_name(name)
                    
                    # format the data
                    self.data[product_code] = {
                        'product_name': product_name,
                        'year': year,
                        'rating': rating
                    }
                    
                end_time = time.time()
                
                print(f'Page {page} of {self.max_pages} done')
                if page == 1:
                    duration = (end_time - start_time) * self.max_pages
                    time_to_complete = datetime.datetime.now() + datetime.timedelta(seconds=duration)
                    print(f'Scraping will be done approximately at {time_to_complete}')
                    
                # update the url to get the next page
                page += 1
                self.url = f'https://www.aperitif.no/pollisten/pollisten-vin-{self.product_type},5,{page}?c[min]=&c[max]=&is_active=1&ordering=points_desc&query='                            
                driver.quit()
                
        except Exception as e:
            print(e)
        
        driver.quit()
        print(f'Product code not found: {wines_skipped}')
        
    def format_product_name(self, name: str):
        name = name.split()
        year = int(name[-1][1:-1]) if name[-1][1:-1].isnumeric() else None
        product_name = ' '.join(name[:-1]) if year is not None else ' '.join(name)
        return product_name, year
    
    def make_dataframe(self):
        self.get_wines()
        df = pd.DataFrame.from_dict(self.data, orient='index')
        
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'product_code'}, inplace=True)
        df.to_excel(f'{self.base_dir}/datasets/{self.product_type}_apertiff.xlsx', index=False)
        return df
        
        
if __name__ == '__main__':
    aperitif = Aperitif('rødvin')
    print(len(aperitif.dataframe))