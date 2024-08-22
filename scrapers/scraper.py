import pandas as pd

from selenium import webdriver

import os
import datetime

class Scraper:
    
    def __init__(self, website_name: str):
        self.website_name = website_name.lower()
        
        self.base_dir = os.path.join(os.path.dirname( __file__ ), '..' )
        
        self.data = {}
        
        self.options = self.setup_driver()
        
    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-search-engine-choice-screen')
        options.add_argument('headless')
        
        return options
    
    def make_dataframe(self):
        df = pd.DataFrame.from_dict(self.data, orient='index')
        
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'product_code'}, inplace=True)
        df.to_excel(f'{self.base_dir}/datasets/{self.website_name}.xlsx', index=False)
        return df
    
    def calculate_time_to_scrape(self, start_time: float, end_time: float, iterations: int):
        duration = (end_time - start_time) * iterations
        time_to_complete = datetime.datetime.now() + datetime.timedelta(seconds=duration)
        print(f'Scraping will be done approximately at {time_to_complete}')
        