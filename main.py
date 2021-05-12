from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time

GOOGLE_DRIVER_PATH = "C:\Development\chromedriver.exe"

headers = {
    "accept": "text/html,application/xhtml+xml,application/"
              "xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}


zillow_endpoint = "https://www.zillow.com/homes/San-Francisco,-CA_rb/?" \
                  "searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22San%" \
                  "20Francisco%2C%20CA%22%2C%22mapBounds%22%3A%7B%22west%22%3A-122.55177535009766" \
                  "%2C%22east%22%3A-122.31488264990234%2C%22south%22%3A37.69926912019228%2C%22north" \
                  "%22%3A37.851235694487485%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A20330" \
                  "%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B" \
                  "%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C" \
                  "%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D" \
                  "%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%" \
                  "7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse" \
                  "%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C" \
                  "%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D" \
                  "%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

google_form_endpoint = "https://docs.google.com/" \
                       "forms/" \
                       "d/" \
                       "e/" \
                       "1FAIpQLSdlbJNe1O0bRxVbP5l_GvcSoTsLGMIFPep9sffX2GG6kbpCWw/" \
                       "viewform?usp=sf_link"

response = requests.get(url=zillow_endpoint, headers=headers)
result = response.text

soup = BeautifulSoup(result, "html.parser")

all_links_tag = soup.select(".photo-cards .list-card-top a")
all_links = []
for link in all_links_tag:
    lnk = link.get("href")
    all_links.append(lnk)

all_price_tag = soup.select(".photo-cards .list-card-price")
all_prices = []
for price in all_price_tag:
    p = price.getText().split()[0]
    if "/" in p:
        p = p.split("/")[0]
    elif "+" in p:
        p = p.split("+")[0]
    all_prices.append(p)

all_address_tags = soup.select(".photo-cards address")
all_address = []

for address in all_address_tags:
    a = address.getText()
    all_address.append(a)


all_data = [
    {
        "address": address,
        "price": price,
        "link": link
    }
    for (address, price, link) in zip(all_address, all_prices, all_links)
]


driver = webdriver.Chrome(executable_path=GOOGLE_DRIVER_PATH)
driver.get(url=google_form_endpoint)
time.sleep(10)

for data in all_data:
    address_input_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    address_input_field.send_keys(data["address"])

    price_per_month_input_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    price_per_month_input_field.send_keys(data["price"])

    link_input_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    link_input_field.send_keys(data["link"])

    submit_button_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div'
    )

    submit_button_field.click()
    time.sleep(10)
    another_form_field = driver.find_element_by_xpath(
        '/html/body/div[1]/div[2]/div[1]/div/div[4]/a'
    )
    another_form_field.click()
    time.sleep(5)

driver.quit()

