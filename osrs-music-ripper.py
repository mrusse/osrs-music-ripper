import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from chromedriver_py import binary_path

svc = webdriver.ChromeService(executable_path=binary_path)
driver = webdriver.Chrome(service=svc)

driver.get("https://oldschool.runescape.wiki/w/Music")
actionChains = ActionChains(driver)
wait = WebDriverWait(driver, 30)
i = 760

links = []

while (True):
    try:
        print(i)
        play = wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[3]/div[3]/div[5]/div[1]/table[3]/tbody/tr[" + str(i) + "]/td[5]/a")))
        text = play.get_dom_attribute("href")
        links.append("https://oldschool.runescape.wiki" + text)
        i += 1
    except Exception as e:
        #print(e)
        break

for link in links:
    print(link)
    driver.get(link)
    download = wait.until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[3]/div[3]/div[5]/div[2]/p/a[2]")))
    download.click()

time.sleep(5)
driver.quit()