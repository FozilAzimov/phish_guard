import requests
from bs4 import BeautifulSoup
import hashlib
import sqlite3
import json
import base64
import re
from urllib.parse import unquote, urlparse


def sus_characters(url):
    decoded_url = unquote(url)
    parsed_url = urlparse(decoded_url)
    print(parsed_url)
    url_characters = parsed_url.netloc + parsed_url.path
    suspicious_characters = re.findall(r'[^\x00-\x7F]', url_characters)
    
    if suspicious_characters:
        return True
    else:
        return False

def analyse_url(url):
    try:
        if sus_characters(url):
            add_link_to_blacklist(url)
            return 'Diqqat! Sayt fishing sahifa ekanligi aniqlandi ‼️\n Sabab: Ushbu havolada shubxali belglilar (kirill harflari yoki boshqalar) aniqlandi.\nIltimos, ushbu havolaga ishonishdan oldin yaxshilab o\'ylab ko\'rishingizni so\'raymiz!'
        if get_blacklist(url):
            return 'Diqqat! Sayt fishing sahifa ekanligi aniqlandi ‼️\n Sabab: Ushbu havola bizning qora ro\'yxatimizga allaqachon kiritilgan.\nIltimos, ushbu havolaga ishonishdan oldin yaxshilab o\'ylab ko\'rishingizni so\'raymiz!'
        if not (url.startswith("https://") or url.startswith("http://")):
            add_link_to_blacklist(url)
            return "🙋‍♂️ Havolaning to'g'ri ekanligiga ishonch hosil qiling, quyidagi havola misol sifatida:\nhttps://example.com yoki http://example.com"
        if len(url) > 100:
            add_link_to_blacklist(url)
            return "Diqqat! Sayt fishing sahifa ekanligi aniqlandi ‼️\n Sabab: Havola uzunligi rasmiy standartlardan uzun, bu esa uning norasmiy (nusxalangan) ya\'ni fishing havola ekanligiga dalil bo\'la oladi.\nIltimos, ushbu havolaga ishonishdan oldin yaxshilab o\'ylab ko\'rishingizni so\'raymiz!"
    except:
        pass    
    # Start real analysis
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    
    image_urls = []
    img_tags = soup.find_all('img')
    
    for img in img_tags:
        src = img.get('src')
        if src:
            if src.startswith('http://') or src.startswith('https://'):
                image_urls.append(__md5(src))
    
    sus_images = check_image_db(image_urls)
    if len(sus_images) > 10:
        add_link_to_blacklist(url)
        return 'Diqqat! Sayt fishing sahifa ekanligi aniqlandi ‼️\nIltimos, ushbu havolaga ishonishdan oldin yaxshilab o\'ylab ko\'rishingizni so\'raymiz!'


def check_image_db(image_checksums):
    conn = sqlite3.connect('images.db')
    results = []
    for checksum in image_checksums:
        cursor = conn.execute("SELECT org_url FROM image_db WHERE hash = '" + checksum + "'")
        for row in cursor:
            results.append(row[0])
    conn.close()
    return json.dumps(results)

def add_link_to_blacklist(url):
    conn = sqlite3.connect('blacklist.db')
    conn.cursor().execute("INSERT INTO blacklist (url) VALUES ('" + base64.b64encode(url.encode("ascii")).decode("ascii") + "');")
    conn.commit()
    conn.close()

def get_blacklist(url):
    conn = sqlite3.connect('blacklist.db')
    cursor = conn.execute("SELECT url FROM blacklist WHERE url = '" + base64.b64encode(url.encode("ascii")).decode("ascii") + "';")
    try:
        for row in cursor:
            if len(row[0]) > 1:
                return True
        return False
    except: return False

def __md5(url):
    response = requests.get(url)
    image_data = response.content
    md5_hash = hashlib.md5(image_data).hexdigest()
    return md5_hash

def analyse_image(img_url, org_url):
    pass