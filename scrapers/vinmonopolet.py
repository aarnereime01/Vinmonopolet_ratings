import pandas as pd
from bs4 import BeautifulSoup as bs

class Vinmonopolet:
    def __init__(self, product_type, ):
        self.product_type = product_type.lower()
        
        
if __name__ == '__main__':
    vinmonopolet = Vinmonopolet('rødvin')
    vinmonopolet.get_data()