import requests as rq
from bs4 import BeautifulSoup, element
from time import sleep

gerne_link = open('text.txt', 'r', encoding='utf-8').readlines()  # Danh sách link thông tin các game
t = open('link_da_chay.txt', 'r', encoding='utf-8').readlines()   # Danh sách các link đã chạy, tránh trùng lặp

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

for link in gerne_link:
    link = link.strip() + '\n'
    
    if link not in t:
        for ii in range(100):
            try: 
                site_raw = rq.get(link, headers=headers)
                if site_raw.status_code == 200: 
                    sub_soup = BeautifulSoup(site_raw.text, "html.parser")
                    h2s = sub_soup.find("div", {"id": "gameGenInfoBox"}).find_all('h2') 
                    temp_tag = element.Tag
                    for h2 in h2s:
                        if h2.string == 'Genre':
                            temp_tag = h2
                    with open('link_da_chay.txt', 'a', encoding='utf-8') as save:
                        save.write(f"{link}")

                    with open('gerne.txt', 'a', encoding='utf-8') as save:
                        save.write(f"{str(temp_tag.next_sibling.string)}\n") # Lọc gerne
                    print(f"Done link: {link}", end="")
                    break
            except:
                sleep(4)