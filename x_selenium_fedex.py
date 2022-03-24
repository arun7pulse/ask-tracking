import requests
import csv
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

# from selenium.webdriver.chrome.options import Options
# CHROME_PATH = ""
# CHROME_DRIVER_PATH = ""
# WINDOW_SIXE = "1920,1080"
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=%s" % WINDOW_SIXE)
# chrome_options = Options()

tlist = []

csvinput = r'c:\users\arannamalai\Desktop\n.csv'
csvinputuniq = csvinput + ".uniq.csv"
csvtemp = csvinput + ".temp.csv"
csvoutput = csvinput + ".processed.csv"


with open(csvinput, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:        # print(row, row[0].split("<BR>"))
        tlist.extend(row[0].split("<BR>"))  # .replace("<BR>", ","))

ulist = list(set(tlist))
print(tlist)
print(ulist)

ulist.sort(reverse=True)

print("TotalList:", len(tlist))
print("UniqList:", len(ulist))

ltrks = []
for item in ulist:
    row = {"tracking": "trk_" + str(item)}
    ltrks.append(row)
# Writing data of CSV file
with open(csvinputuniq, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=',')  # create the csv writer
    for line in ltrks:
        res = writer.writerow(line.values())

lups = []
lusps = []
lfedex = []

for item in ulist:
    if len(item) == 18 and str(item).startswith('1Z'):
        lups.append(item)
    if len(item) == 22 and str(item).startswith('94'):
        lusps.append(item)
    if len(item) == 22 and str(item).startswith('92'):
        lfedex.append(item)
    if len(item) == 12 and str(item).startswith('5'):
        lfedex.append(item)


print("UPS:", len(lups))
print("USPS:", len(lusps))
print("Fedex:", len(lfedex))


ulist = lfedex
chunk = 30
start = 0  # run until 270 again 540
end = 60  # len(ulist)+chunk

# driver = webdriver.Chrome("c:\chromedriver.exe")
# driver.maximize_window()

new_list = []
for j in range(start, end, chunk):
    # for j in range(start, 271, chunk):
    if start == j:
        continue
    litems = ulist[start:j]
    print(start, j)
    start = j
    trackings = ",".join(str(e) for e in litems)
    print(trackings)
    driver = webdriver.Chrome("c:\chromedriver.exe")
    driver.maximize_window()
    # url = 'https://www.fedex.com/fedextrack/summary?trknbr=563718254277,563718251360,563718275128,563718278344,563718251407,563718251679,563718252388,563718251613,563718280079,563718255300,563718282807,563718253899,563718283332,563718256902,563718275209,563718276570,563718280951,563718256214,563718278491,563718279010,563718256795,563718252469,563718279568,563718279774,563718283870,563718281292,563718256270,563718281156,563718280859,563718280734'
    url = "https://www.fedex.com/fedextrack/"

    # driver.find_element_by_id("tracking-input").send_keys("9274810664286610005250,9400111899561210370768,9400111899561210370959")
    driver.get(url)
    time.sleep(10)
    driver.find_element_by_xpath(
        "//button[contains(@class,'fdx-c-navbar__menu__item__button')]").click()
    # driver.find_element_by_xpath("//div[contains(@class,'form-input__element ng-pristine ng-valid ng-touched')]").send_keys(s)
    # driver.find_element_by_xpath("//input[contains(@class,'form-input')]").send_keys(s)
    driver.find_element_by_xpath(
        "//input[contains(@class,'form-input')]").send_keys("563717898438")

    driver.find_element_by_xpath(
        "//button[contains(@class,'fdx-c-button fdx-c-button--primary fdx-c-button--responsive')]") .click()
    time.sleep(25)

    # for elem in driver.find_elements_by_xpath('.//div[@id = "tracked-numbers"]'):
    #     print(driver.find_elements_by_xpath('.//span[@class = "tracking-number"]')[0].text, driver.find_elements_by_xpath('.//div[@class = "delivery_status"]')[0].text.split("\n")[1])
    for elem in driver.find_elements_by_xpath(".//div[contains(@class,'track-bar-container')]"):
        # print(driver.find_elements_by_xpath('.//span[@class = "tracking-number"]')[0].text, driver.find_elements_by_xpath('.//div[@class = "delivery_status"]')[0].text.split("\n")[1])
        print(elem.find_elements_by_xpath('.//span[@class = "tracking-number"]')[
            0].text, ",", elem.find_elements_by_xpath('.//div[@class = "delivery_status"]')[0].text.split("\n")[1])
    driver.close()

    # with open(r'c:\users\arannamalai\Desktop\new.csv', 'a') as f:
    #     # create the csv writer
    #     writer = csv.writer(f)
    #     # write a row to the csv file
    #     writer.writerow(str(elem.find_elements_by_xpath('.//span[@class = "tracking-number"]')[0].text,",", elem.find_elements_by_xpath('.//div[@class = "delivery_status"]')[0].text.split("\n")[1]))

    # driver.close()


# Fedex Authentication

url = "https://apis-sandbox.fedex.com/oauth/token"

payload = input  # 'input' refers to JSON Payload
headers = {
    'Content-Type': "application/x-www-form-urlencoded"
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)


url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"

payload = input  # 'input' refers to JSON Payload
headers = {
    'Content-Type': "application/json",
    'X-locale': "en_US",
    'Authorization': "Bearer "
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
