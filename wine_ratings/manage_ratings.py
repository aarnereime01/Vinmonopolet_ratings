# %%
import pandas as pd

# %%
aperitif = pd.read_excel('/Users/arnereime/Documents/Vinmonopolet_ratings/datasets/rødvin_aperitif.xlsx')
vinmonopolet = pd.read_excel('/Users/arnereime/Documents/Vinmonopolet_ratings/datasets/rødvin_vinmonopolet.xlsx')

# %%
new_df = pd.merge(aperitif, vinmonopolet, on='product_code', how='inner')
# make price column to int
new_df['price'] = new_df['price'].astype(int)
print(new_df.shape)

print(new_df.head())
# %%
# import plotly.express as px
import hvplot.pandas
new_df.hvplot(kind="scatter", 
          x="price", y="rating", by="country", 
          hover_cols=['product_name_x', 'year_x'], 
          grid=True, alpha=0.4, height=800, width=1200)

# fig = px.scatter(new_df, x='price', y='rating', title='Comparison of ratings', hover_name='product_name_x', height=800, width=1200)

# # Add custom data containing wine names to each point
# fig.update_traces(customdata=new_df['product_name_x'])

# # Customize hover template to display wine names
# fig.update_traces(hovertemplate='Price: %{x}<br>Rating: %{y}<br>%{customdata}<extra></extra>')

# fig.show()
# %%


test_data_set = vinmonopolet[:10].copy()
print(test_data_set)

# %%
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time
from selenium.webdriver.common.keys import Keys

base_dir = os.path.join(os.path.dirname( __file__ ), '..' )
chrome_driver_path = os.path.join(base_dir, 'chromedriver')

service = Service(executable_path=chrome_driver_path)
options = webdriver.ChromeOptions()
options.add_argument("window-size=1920,1080")
# options.add_argument('headless')
        
url = 'https://www.wineenthusiast.com/'
# %%
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

# click on the input to activate the search bar
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-wrapper')))
driver.find_element(By.CLASS_NAME, 'search-wrapper').click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ais-SearchBox-input')))
input_element = driver.find_element(By.CLASS_NAME, 'ais-SearchBox-input')
input_element.send_keys('stags leap' + Keys.ENTER)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ratings-tab')))
ratings_tab = driver.find_element(By.ID, 'ratings-tab')
ratings_tab.click()

# check if there are any ratings

results = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'search-total-hits')))
print(results[1].text)

time.sleep(1000)


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

driver.quit()


# %%
driver = webdriver.Chrome(service=service, options=options)
driver.get(url)

# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ais-SearchBox-input')))

driver.find_element(By.CLASS_NAME, 'ais-SearchBox-input')
driver.find_element(By.CLASS_NAME, 'ais-SearchBox-submit').click()

print(driver.page_source)
driver.quit()
# %%

import Levenshtein as lev

compare1 = "Stag's Leap Wine Cellars 2015 Cask 23 Cabernet Sauvignon (Stags Leap District)"
compare2 = "Stag's Leap Cask 23 Cabernet Sauvignon 2005"

print(lev.ratio(compare1, compare2))
# %%
