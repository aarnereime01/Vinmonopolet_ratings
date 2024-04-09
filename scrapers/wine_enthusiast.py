from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
import time
import datetime

class WineEnthusiast:
    
    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname( __file__ ), '..' )
        self.chrome_driver_path = os.path.join(self.base_dir, 'chromedriver')
        
        self.vinmonopolet = pd.read_excel('/Users/arnereime/Documents/Vinmonopolet_ratings/datasets/rødvin_vinmonopolet.xlsx')
        self.data = {}
        self.i = 0
        
        self.base_url = 'https://www.wineenthusiast.com/'
        self.url = f'https://www.wineenthusiast.com/'

        self.dataframe = self.make_dataframe()
        
    def get_wines(self, wine_name: str, year: float = np.nan):
        start_time = time.time()
        if np.isnan(year):
            wine_to_check = wine_name
        else:
            wine_to_check = wine_name + ' ' + str(int(year))
        
        try:
            service = Service(executable_path=self.chrome_driver_path)
            options = webdriver.ChromeOptions()
            options.add_argument("window-size=1920,1080")
            options.add_argument('headless')
                    
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(self.url)

            # click on the input to activate the search bar
            driver.find_element(By.CLASS_NAME, 'search-wrapper').click()

            # search for the wine
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ais-SearchBox-input')))
            input_element = driver.find_element(By.CLASS_NAME, 'ais-SearchBox-input')
            input_element.send_keys(wine_to_check + Keys.ENTER)

            # navigate to the ratings tab
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ratings-tab')))
            ratings_tab = driver.find_element(By.ID, 'ratings-tab')
            ratings_tab.click()
            
            # check if there are any ratings
            results = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-total-hits')))
            total_search_results = results[1].text
            if total_search_results == '0':
                print('No wine found for wine:', wine_to_check)
                self.i += 1
                driver.quit()
                return
            
            # click on the first wine
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ratings-block__info')))
            h3_element = driver.find_element(By.CLASS_NAME, "ratings-block__info")
            link_element = h3_element.find_element(By.TAG_NAME, "a")
            link_element.click()

            # get page content
            html = driver.page_source
            soup = bs(html, 'html.parser')

            name = soup.find('h1', {'class': 'review-title'}).text
            print(name.strip())

            rating = soup.find('div', {'class': 'score'}).find('div', {'class': 'value'})
            print(rating.text.strip())

            where_from = soup.find('div', {'class': 'winery-location d-flex align-content-center'})
            yo = [x.strip() for x in where_from.text.split(',')]
            print(yo)

            volume = soup.find('div', {'class': 'bottle-size'}).find('div', {'class': 'value'})
            print(volume.text.strip())
            self.i += 1
            driver.quit()
            end_time = time.time()
            print(f'Wine {self.i} done')
            if self.i == 1:
                    duration = (end_time - start_time) * self.vinmonopolet.shape[0]
                    time_to_complete = datetime.datetime.now() + datetime.timedelta(seconds=duration)
                    print(f'Scraping will be done approximately at {time_to_complete}')
        except Exception as e:
            self.i += 1
            driver.quit()
            print('No wine found for wine:', wine_to_check)
        
    def make_dataframe(self):
        yo = self.vinmonopolet.apply(lambda x: self.get_wines(x['product_name'], x['year']), axis=1)
            
if __name__ == '__main__':
    we = WineEnthusiast()
