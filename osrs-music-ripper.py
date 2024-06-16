import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from urllib.request import unquote
from urllib.request import Request, urlopen

response = requests.get("https://oldschool.runescape.wiki/w/Music")
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

hrefs = soup.find_all('a', href=True)
hrefs = [link['href'] for link in hrefs if link['href'].endswith('.ogg')]
title_max_length = len(max(hrefs, key = len).split("File:")[1])

for href in (bar := tqdm(hrefs, desc = "Downloading: ", bar_format='{desc}{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')):
    title = href.split("File:")[1]
    link = "https://oldschool.runescape.wiki/images/" + title

    title = unquote(title)
    bar.set_description("Downloading Song - " + str(title).ljust(title_max_length))
    
    req = Request(
        url=link, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    oggfile = urlopen(req)
    with open("music\\" + str(title),'wb') as output:
        output.write(oggfile.read())