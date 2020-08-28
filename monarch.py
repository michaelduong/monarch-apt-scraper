# Monarch Apartment Price Scraper

# Monarch.py
# Checks Monarch apartment webpages every hour to see if the prices have changed

import bs4
import requests
import smtplib
import time

# time between checks in seconds
sleeptime = 3600

# generic network request function that returns an array of prices
def getPrices(floorplan: str) -> [str]:
    url = "https://www.themonarchbywindsor.com/floorplans/" + floorplan
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    web_page = bs4.BeautifulSoup(response.content, 'html.parser')
    price = web_page.find_all(class_="td-card-rent")

    results = [r.text.split(' ')[0].strip() for r in price]
    results = [result.replace("Rent:", "") for result in results]

    return results

def sendEmail(floorplan: str):
    msg = "Subject: Monarch's " + floorplan.capitalize() + " price has changed!"
    fromaddr = '[GMAIL EMAIL ADDRESS HERE]'
    toaddr = ['[EMAIL ADDRESS TO SEND TO]']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("[GMAIL EMAIL ADDRESS HERE]", "[GMAIL EMAIL PASSWORD HERE]")
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

last_A4_Prices = None
last_A1D_Prices = None

currentA4Prices = getPrices("a4")
currentA1DPrices = getPrices("a1d")

if last_A4_Prices is None:
    last_A4_Prices = currentA4Prices
if last_A1D_Prices is None:
    last_A1D_Prices = currentA1DPrices

while True:
    if last_A1D_Prices == currentA1DPrices or last_A4_Prices == currentA4Prices:
        print("No price change")
    if last_A1D_Prices != currentA1DPrices:
        print("Price has changed!")
        sendEmail("a1d")
        if last_A4_Prices != currentA4Prices:
            print("Price has changed!")        
            sendEmail("a4")
    time.sleep(sleeptime)