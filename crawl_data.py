import requests as rq
from bs4 import BeautifulSoup, element
import pandas as pd
import numpy as np
import pytz
from datetime import *

pages = 329    #số page cần chạy 
page_start = 1 #page bắt đầu
result = 200   #số game trên mỗi trang

def convertTimeVN():
    vn_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    current_time_vn = datetime.now(vn_tz)
    return current_time_vn

urlh = "https://www.vgchartz.com/games/games.php?page="
urlt = f"&results={result}&order=TotalSales&ownership=Both&direction=DESC&showtotalsales=1&shownasales=1&showpalsales=1&showjapansales=1&showothersales=1&showpublisher=1&showdeveloper=0&showreleasedate=1&showlastupdate=0&showvgchartzscore=0&showcriticscore=0&showuserscore=0&showshipped=0"

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

# # Khởi tạo các cột (bỏ cmt nếu muốn chạy lại từ đầu)
# columns = ['Rank', 'Name', 'Platform', 'Year', 'Publisher', 'NA_Sales', 'PAL_Sales', 'JP_Sales', 'Other_Sales', 'Global_Sales']
# df = pd.DataFrame(columns=columns)
# df.to_csv("data.csv", mode='w', index=False, encoding='utf-8')


# Duyệt từng page
for page in range(page_start , pages + 1):
    url = urlh + str(page) + urlt
    print(f"[{str(convertTimeVN()).split(' ')[1].split('.')[0]}]", end= " - ")
    print(f"Get data from page {page} ........ ", end= "")

    try:
        # thử request
        for ii in range(0, 5):
            data = rq.get(url=url, headers= headers)
            if data.status_code == 200:
                rank, gname, platform, year, genre, publisher = [], [], [], [], [], []
                sales_na, sales_pal, sales_jp, sales_ot, sales_gl = [], [], [], [], []
                soup = BeautifulSoup(data.text, 'html.parser')     #Sử dụng BeautifulSoup xử lý html
                game_tags = soup.find_all('a', href=lambda href: href and '/game/' in href)  #Lấy thông tin các game
                gname = [name.get_text(strip=True) for name in game_tags]

                for tag in game_tags:
                    # Lấy thông tin mỗi game
                    data = tag.parent.parent.find_all("td")
                    rank.append(data[0].string)
                    platform.append(data[3].find('img').attrs['alt'] if data[3] and data[3].find('img') else "N/A") #arrrs: lấy giá trị của thuộc tính
                    publisher.append(data[4].string if not data[4].string.startswith("N/A") else "N/A")
                    sales_na.append(data[6].string[:-1] if not data[6].string.startswith("N/A") else "0")
                    sales_pal.append(data[7].string[:-1] if not data[7].string.startswith("N/A") else "0")
                    sales_jp.append(data[8].string[:-1] if not data[8].string.startswith("N/A") else "0")
                    sales_ot.append(data[9].string[:-1] if not data[9].string.startswith("N/A") else "0")
                    sales_gl.append(data[5].string[:-1] if not data[5].string.startswith("N/A") else "0")

                    release_year = data[10].string.split()[-1]
                    if release_year.startswith("N/A"):
                        year.append("N/A")
                    else:
                        if int(release_year) >= 30:
                            year_to_add = ("19" + release_year)
                        else:
                            year_to_add = ("20" + release_year)
                        year.append(year_to_add)

                    url_to_game = tag.attrs['href']
                    genre.append(url_to_game)  #Lấy link thông tin mỗi game

                with open('text.txt', 'a', encoding='utf-8') as save:
                    for g in genre:
                        save.write(f"{g}\n")
                df_page = pd.DataFrame({
                    'Rank': rank,
                    'Name': gname,
                    'Platform': platform,
                    'Year': year,
                    'Publisher': publisher,
                    'NA_Sales': sales_na,
                    'PAL_Sales': sales_pal,
                    'JP_Sales': sales_jp,
                    'Other_Sales': sales_ot,
                    'Global_Sales': sales_gl
                })

                df_page.to_csv("data.csv", mode='a', index=False, header=False, encoding='utf-8')
                print(" -> Success")
                break
    except:
        print(" -> Fail")
        break
