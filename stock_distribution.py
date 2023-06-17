from bs4 import BeautifulSoup
import time
import requests

class Data():
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        })

    def get_stock_data(self, stock_code):
        url = f'https://fundamentus.com.br/detalhes.php?papel={stock_code}'
        response = self.session.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        stock_data = soup.find('td', class_="data destaque w3")
        if stock_data is not None:
            stock_price = float(stock_data.text.strip().replace(',', '.'))
            print(f'The value of {stock_code} is: R${stock_price}')
            return stock_price
        else:
            print(f"Data for stock {stock_code} not found")
            return None

    def ideal_investment_by_quantity(self, prices, quantity):
        investment = 0
        for stock, price in prices.items():
            investment += price * quantity
        return investment

    def distribute_investment(self, prices, investment):
        distribution = {}
        remaining = investment  
        investment_per_company = investment / len(prices)

        for stock, price in prices.items():
            stock_quantity = investment_per_company // price  
            distribution[stock] = stock_quantity
            remaining -= stock_quantity * price  

        return distribution, remaining

    
    def run_all(self):
        stock_codes_input = input('Enter the stock codes you want to search for (separate by commas): ')
        stock_codes = [code.strip() for code in stock_codes_input.split(',')]
        prices = {}
        for code in stock_codes:
            price = self.get_stock_data(code)
            if price is not None:
                prices[code] = price
            time.sleep(2)
        ideal_investment_choice = input('Do you want to calculate the ideal investment? (yes/no)')
        if ideal_investment_choice.lower() == 'yes':
            quantity = int(input('How many stocks would you like to buy from each company?'))
            ideal_investment = self.ideal_investment_by_quantity(prices, quantity)
            print(f'The ideal investment to buy {quantity} stocks from each company is R${ideal_investment}')

        investment_choice = input('Would you like to inform the amount you want to invest? (yes/no)')
        if investment_choice.lower == 'yes':
            investment = float(input('How much do you want to invest?').replace(',', '.'))
            distribution, remaining = self.distribute_investment(prices, investment)

        for stock, quantity in distribution.items():
            print(f'You can buy {quantity} stocks of {stock} with R${investment}')
    
        print(f'You have R${remaining:.2f} left from your initial investment.')

# To run
Data().run_all()
