import requests
import music_tag
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

for i, href in enumerate(bar := tqdm(hrefs, desc = "Downloading: ", bar_format='{desc}{percentage:3.0f}% |{bar}| {n_fmt}/{total_fmt}')):
    title = href.split("File:")[1]
    link = "https://oldschool.runescape.wiki/images/" + title

    composer = requests.get("https://oldschool.runescape.wiki/w/" + title.replace(".ogg",""))

    if ("Composer" in composer.text):
        composer = composer.text.split("Composer")[1].split("\n")[2].split(">")[1].replace("<small","")
    else:
        composer = requests.get("https://oldschool.runescape.wiki/w/" + title.replace(".ogg","") + "_(music_track)")
        composer = composer.text.split("Composer")[1].split("\n")[2].split(">")[1].replace("<small","")

    title = unquote(title)
    bar.set_description("Downloading Song - " + str(title).ljust(title_max_length))
    title = str(title).replace("_", " ")
    
    req = Request(
        url=link, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )

    oggfile = urlopen(req)
    with open("music\\" + title,'wb') as output:
        output.write(oggfile.read())
    
    song = music_tag.load_file("music\\" + title)
    song['title'] = title.split(".ogg")[0]
    song['album'] = "Unofficial Old School RuneScape Soundtrack"
    song['artist'] = composer
    song.raw['tracknumber'] = str(i+1).zfill(3)

    with open('cover.jpg', 'rb') as cover:
        song['artwork'] = cover.read()
    
    song.save()