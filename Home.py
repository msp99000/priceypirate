import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot
import streamlit as st
import pandas as pd
import datetime
from styles import streamlit_style
from time import sleep
import asyncio
from playwright.async_api import async_playwright
# from telebot import auth
from telebot import send_telegram_message
from messages import flipkart_msg, amazon_msg
from streamlit import session_state as state

streamlit_style()


if 'df' not in state:
    state['df'] = pd.DataFrame(columns=['Time','Product', 'Price','Discount', 'Status','Date'])

texter = [1,2,3]

state['texter'] = [7,8,9]

tracker = False

async def get_page(link):
    # auth = auth
    auth = st.secrets['auth']
    browser_url = f'wss://{auth}@brd.superproxy.io:9222'
    async with async_playwright() as pw:
        print('connecting');
        browser = await pw.chromium.connect_over_cdp(browser_url)
        print('connected');
        page = await browser.new_page()
        print('goto')
        await page.goto(link, timeout=120000)
        print('done, evaluating')
        print(await page.evaluate('()=>document.documentElement.outerHTML'))
        await browser.close()

# asyncio.run(main())

def get_amazon_details(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Fetch item details
    # try:
    item_name = soup.find('span', {'id': 'productTitle'}).get_text().strip()
    item_price = soup.find('span', {'class': 'a-offscreen'}).get_text().strip()
    item_discount = soup.find('span', {'class': 'a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage'}).get_text().strip()
        # item_status = 
    # except:
    return item_name, item_price, item_discount


def get_flipkart_details(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Fetch item details
    try:
        item_name = soup.find('span', {'class': 'B_NuCI'}).get_text().strip()
    except Exception:
        item_name = "N/A"   

    try:
        item_price = soup.find('div', {'class': '_30jeq3 _16Jk6d'}).get_text().strip()
    except Exception as e:
        item_price = "N/A"

    try:
        item_discount = soup.find('div', {'class': '_3Ay6Sb _31Dcoz'}).get_text().strip()
    except:
        item_discount = "N/A"   

    try:
        item_status = soup.find('div', {'class': '_16FRp0'}).get_text().strip()
    except:
        item_status = "Available"

    # return item_name, item_price, item_discount, status

    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().date()
    message = flipkart_msg(item_name, item_price, item_discount, item_status, url, current_time)
    state.df.loc[len(state.df)] = [current_time,
                                   item_name,
                                   float(item_price[1:].replace(',', '')),
                                   item_discount[:3],
                                   item_status,
                                   current_date]



 
def check_price_change(df, interval=60):
    previous_prices = {}
    while tracker == True:
        for product in df['Product'].unique():
            product_df = df[df['Product'] == product]
            # Get the latest price for the product
            latest_price = product_df['Price'].iloc[-1]
            # Get the previous price for the product
            previous_price = previous_prices.get(product)
            # Check for price change
            if previous_price is not None and latest_price != previous_price:
                print("Price has changed for", product)
                print("Previous price:", previous_price)
                print("Latest price:", latest_price)
                # Add your alert mechanism here (e.g., sending an email, displaying a notification, etc.)

            # Update the previous price for the product
            previous_prices[product] = latest_price

        # Wait for the specified interval before checking again
        time.sleep(interval)

# Function to process the uploaded file based on the selected option
def process_file(selected_option, uploaded_file):
    if selected_option == 'Amazon':
        # Process Amazon file
        process_amazon_file(uploaded_file)
    elif selected_option == 'Flipkart':
        # Process Flipkart file
        process_flipkart_file(uploaded_file)

# Function to process the Amazon file
def process_amazon_file(uploaded_file):
    # Read and process the Amazon file
    content = uploaded_file.read().decode('utf-8').split('\n')
    # Process the content and display the output
    for url in content:
        amazon_name, amazon_price, amazon_discount = get_amazon_details(f'{url}')
        amz_msg = amazon_msg(amazon_name, amazon_price, amazon_discount)
        st.write(amz_msg)

# Function to process the Flipkart file
def process_flipkart_file(uploaded_file):
    # Read and process the Flipkart file
    content = uploaded_file.read().decode('utf-8').split('\n')
    # Process the content and display the output
    counter = 0
    while counter < 10:
        for link in content:
            get_flipkart_details(link)
        # unique_products = state.df['Product'].unique()
        # for product in unique_products:
        #     product_df = state.df[state.df['Product'] == product].sort_values('Time')
        #     price_changes = product_df['Price'].diff().dropna()
        #     percentage_changes = (price_changes / product_df['Price'].shift()) * 100
        #     for index, change in enumerate(price_changes):
        #         st.write(f"Product: {product}")
        #         st.write(f"Price Change: {change}")
        #         st.write(f"Discount (%): {percentage_changes.iloc[index]:.2f}%")
        #         st.write(f"Time: {product_df.iloc[index + 1]['Time']}")
        #         st.subheader(" ")
        # counter += 1
        # time.sleep(1 * 60)

        previous_prices = {}
        for product in state.df['Product'].unique():
            product_df = state.df[state.df['Product'] == product]
            # Get the latest price for the product
            latest_price = product_df['Price'].iloc[-1]
            latest_status = product_df['Status'].iloc[-1]
            # Get the previous price for the product
            previous_price = previous_prices.get(product)
            # Check for price change
            if previous_price is not None and latest_price != previous_price:
                st.write("Price has changed for : ", product)
                st.write("Previous price : ", previous_price)
                st.write("Latest price : ", latest_price)
                st.write("Latest status : ", latest_status)
                # Add your alert mechanism here (e.g., sending an email, displaying a notification, etc.)
            else:
                st.subheader(f'Timestamp : {datetime.datetime.now().strftime("%H:%M:%S")}')
                st.write(f"Product : {product}")
                st.write(" ")
                st.write(f"Status : {latest_status}")
                st.write(" ")
                st.write(f'No price changes detected! Notified on Telegram')
                st.subheader(" ")
                asyncio.run(send_telegram_message(f"No price changes detected for {product} and the latest status is {latest_status}"))

            # Update the previous price for the product
            previous_prices[product] = latest_price

            counter += 1
            time.sleep(20)

    # st.dataframe(state.df)


# Main Streamlit code
def main():
    # Title and description
    st.title("Pricey Pirate Web Scrapper Pro")
    st.write("Select an option and upload the corresponding file.")

    # Select box for options
    selected_option = st.selectbox("Select an option", ('Amazon', 'Flipkart'))

    # File uploader
    uploaded_file = st.file_uploader(f"Upload {selected_option} file", type='txt')

    # Process the uploaded file when the user clicks the "Submit" button
    if st.button('Start Tracking'):
        if uploaded_file is not None:
            success = st.success("Tracker Started!", icon='✅')
            # asyncio.run(send_telegram_message("Tracker Started"))
            process_file(selected_option, uploaded_file)
            success.empty()

        
# Run the Streamlit app
if __name__ == '__main__':
    main()

