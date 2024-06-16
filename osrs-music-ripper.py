import time
import urllib.request
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from chromedriver_py import binary_path
from urllib.request import Request, urlopen

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless=new')
chrome_options.add_argument('log-level=3')
chrome_options.page_load_strategy = 'eager'

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc, options=chrome_options)

driver.get("https://oldschool.runescape.wiki/w/Music")
actionChains = ActionChains(driver)
wait = WebDriverWait(driver, 10)

links = []
hrefs = driver.find_elements(By.LINK_TEXT, "Play track")

for href in (bar := tqdm(hrefs, desc = "Downloading: ", bar_format='{desc}{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')):
    song = href.get_dom_attribute("href").split("File:")[1]
    link = "https://oldschool.runescape.wiki/images/" + song
    bar.set_description("Downloading Song - " + song)

    req = Request(
        url=link, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    oggfile = urlopen(req)
    with open("Music\\"+song,'wb') as output:
        output.write(oggfile.read())

driver.quit()