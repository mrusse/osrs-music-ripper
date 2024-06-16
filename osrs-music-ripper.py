import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from chromedriver_py import binary_path

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless=new')
chrome_options.page_load_strategy = 'eager'

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc, options=chrome_options)

driver.get("https://oldschool.runescape.wiki/w/Music")
actionChains = ActionChains(driver)
wait = WebDriverWait(driver, 10)

links = []
hrefs = driver.find_elements(By.LINK_TEXT, "Play track")

for href in tqdm(hrefs, desc="Gathering Song Links: ", bar_format='{desc}{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}'):
    links.append("https://oldschool.runescape.wiki" + href.get_dom_attribute("href"))

song_links = tqdm(links, bar_format='{desc}{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')

for link in song_links:
    song_links.set_description("Downloading Song - " + link.split("File:")[1])
    driver.get(link)

    while(True):
        try:
            download = wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div[3]/div[5]/div[2]/p/a[2]")))
            break
        except:
            driver.refresh()
            continue

    download.click()

time.sleep(5)
driver.quit()