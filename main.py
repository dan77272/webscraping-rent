import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time

URL = "https://www.zillow.com/mississauga-on/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Mississauga%2C%20ON%22%2C%22mapBounds%22%3A%7B%22west%22%3A-79.8804965756836%2C%22east%22%3A-79.47880895361328%2C%22south%22%3A43.46165380016259%2C%22north%22%3A43.661178333840546%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A792679%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
response = requests.get(URL, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"})
zillow_website = response.text
soup = BeautifulSoup(zillow_website, "html.parser")

s = Service('C:\Development\chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get(GOOGLE_SHEET)
driver.maximize_window()

my_list = soup.findAll(name="a", class_="list-card-link")
my_list2 = []
price_list = soup.findAll(class_='list-card-price')
price_list2 = []
address_list = soup.findAll(name="img")
address_list2 = []

for x in my_list[:9]:
    if str(x['href'][0]) == '/':
        my_list2.append(f"https://www.zillow.com/{x['href']}")
    else:
        my_list2.append(x['href'])

for x in price_list:
    price_list2.append(x.getText().split()[0])

for x in address_list:
    if "Mississauga" in str(x):
        address_list2.append(x['alt'])

print(my_list2)
print(price_list2)
print(address_list2)

for x in range(len(my_list2)):
    address = driver.find_element(By.XPATH,
                                  '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price = driver.find_element(By.XPATH,
                                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link = driver.find_element(By.XPATH,
                               '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    address.send_keys(address_list2[x])
    price.send_keys(price_list2[x])
    link.send_keys(my_list2[x])
    submit.click()
    time.sleep(2)
    driver.get('https://docs.google.com/forms/d/e/1FAIpQLSdSKOB5AAT-YAlzQDs21Ucc0G-0FJr9EvXJT6yYNkgr3zB3yw/viewform')
    time.sleep(2)
