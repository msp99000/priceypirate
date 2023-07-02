import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot
from creds import * 

def get_amazon_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Fetch item details
    item_name = soup.find('span', {'id': 'productTitle'}).get_text().strip()
    item_price = soup.find('span', {'class': 'a-offscreen'}).get_text().strip()
    item_discount = soup.find('span', {'class': 'a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage'}).get_text().strip()
    
    return item_name, item_price, item_discount

def get_flipkart_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Fetch item details
    item_name = soup.find('span', {'class': '_35KyD6'}).get_text().strip()
    item_price = soup.find('div', {'class': '_30jeq3 _1_WHN1'}).get_text().strip()
    item_discount = soup.find('div', {'class': '_3Ay6Sb _31Dcoz'}).get_text().strip()
    
    return item_name, item_price, item_discount

# Fetch Amazon details
amazon_url = input("Enter the Amazon URL: ")
amazon_name, amazon_price, amazon_discount = get_amazon_details(amazon_url)
print("\n(Amazon)")
print("\nName:", amazon_name)
print("\nPrice:", amazon_price)
print("\nDiscount:", amazon_discount)
print("\n---------------------------------------------------------------------------\n\n")

# Fetch Flipkart details
# flipkart_name, flipkart_price, flipkart_discount = get_flipkart_details(flipkart_url)
# print("Flipkart:")
# print("Name:", flipkart_name)
# print("Price:", flipkart_price)
# print("Discount:", flipkart_discount)


