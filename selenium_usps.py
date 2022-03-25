import json
import csv
import time
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import *

chromedriver = r".\chromedriver.exe"
inputcsv = r'.\input.csv'
inputcsvuniq = inputcsv + ".uniq.txt"
outputcsv = r".\output.csv"
outputjson = r".\output.json"

options = Options()
options.add_argument("start-maximized")
s = Service(chromedriver)
driver = webdriver.Chrome(service=s, options=options)
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


tlist = []
with open(inputcsv, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:        # print(row, row[0].split("<BR>"))
        tlist.extend(row[0].split("<BR>"))  # .replace("<BR>", ","))

ulist = list(set(tlist))
print("TotalList", tlist)
print("\nUniqList", ulist)

ulist.sort(reverse=True)

print("TotalList:", len(tlist), "UniqList:", len(ulist))

ltrks = []
for item in ulist:
    row = {"tracking": "trk_" + str(item)}
    ltrks.append(row)

# Writing data of CSV file
with open(inputcsvuniq, 'w', encoding='UTF8', newline='') as f:
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

ulist = lusps

chunk = 30
start = 0  # run until 270 again 540
end = len(ulist)+chunk

# driver = webdriver.Chrome(chromedriver)# driver.maximize_window()

# Create json file if not exist.
with open(outputjson, "w") as jsonFile:
    json.dump({"tracking":"status"}, jsonFile)
# result_csv = []
for j in range(start, end, chunk):
    if start == j:
        continue
    litems = ulist[start:j]
    print(start, j)
    start = j
    trackings = ",".join(str(e) for e in litems)
    print(trackings)
    # driver.find_element_by_id("tracking-input").send_keys("9274810664286610005250,9400111899561210370959")
    driver.get("https://tools.usps.com/go/TrackConfirmAction_input")
    # driver.find_element_by_xpath("//button[contains(@class,'tracking-btn')]").click()
    driver.find_element(By.ID, "tracking-input").send_keys(trackings)
    driver.find_element(
        by=By.XPATH, value="//button[contains(@class,'tracking-btn')]").click()
    time.sleep(25)
    # Load the json file with new status.
    with open(outputjson, "r") as jsonFile:
        result_json = json.load(jsonFile)

    # for elem in driver.find_element(by=By.XPATH, value=".//div[contains(@class,'track-bar-container')]"):
    for elem in driver.find_elements_by_xpath(".//div[contains(@class,'track-bar-container')]"):
        # print(elem.find_elements_by_xpath('.//span[@class = "tracking-number"]')[0].text,",", elem.find_elements_by_xpath('.//div[@class = "delivery_status"]')[0].text.split("\n")[1])
        print(elem.find_element(by=By.XPATH, value='.//span[@class = "tracking-number"]').text, ",", elem.find_element(
            by=By.XPATH, value='.//div[@class = "delivery_status"]').text.split("\n")[1])         #  ,",", elem.find_element(by=By.XPATH, value='.//div[@class = "delivery_status"]').text.split("\n")[2] )

        # result_csv.append({"tracking": "trk_" + str(elem.find_element(by=By.XPATH, value='.//span[@class = "tracking-number"]').text),
        #        "status": elem.find_element(by=By.XPATH, value='.//div[@class = "delivery_status"]').text.split("\n")[1]})

        result_json[str(elem.find_element(by=By.XPATH, value='.//span[@class = "tracking-number"]').text)] = elem.find_element(by=By.XPATH, value='.//div[@class = "delivery_status"]').text.split("\n")[1]

    # Load the json file with existing status.
    with open(outputjson, "w") as jsonFile:
        json.dump(result_json, jsonFile)
        
# pprint(result_json)
driver.close()

with open(outputcsv, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=',')  # create the csv writer
    # res = writer.writerow(['tracking', 'status'])
    for tracking in result_json.items():
        res = writer.writerow(tracking)
