from requests.adapters import HTTPAdapter
import re
from bs4 import BeautifulSoup
import requests


# get all translation
def get_translation(keyword):
    session = requests.Session()
    block_list = []
    translation_list = []
    uk_pron, uk_mp3, us_pron, us_mp3 = "No UK pronounce", "None", "No US pronounce", "None"

    url = 'https://dictionary.cambridge.org/zhs/%E8%AF%8D%E5%85%B8/%E8%8B%B1%E8%AF%AD-%E6%B1%89%E8%AF%AD-%E7%AE%80%E4%BD%93/' + keyword

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/88.0.4324.104 Safari/537.36"
    }

    session.mount('http://', HTTPAdapter(max_retries=3))
    session.mount('https://', HTTPAdapter(max_retries=3))
    source_html_text = session.get(url, headers=headers).text
    soup = BeautifulSoup(source_html_text, "html.parser")

    # 词性 + 中英翻译的 class 提取出来放入一个列表
    if soup.find_all("div", class_='pr entry-body__el'):
        word_block = soup.find_all("div", class_='pr entry-body__el')

        uk = soup.find_all('span', class_='uk dpron-i')
        uk_pron = BeautifulSoup(str(uk[0]), features='lxml').get_text()
        if re.search(r'/(.*)/', uk_pron):
            uk_pron = re.search(r'/(.*)/', uk_pron).group(0)
        else:
            uk_pron = "No UK pronounce"

        if re.search(r'src="(.*)mp3', str(uk[0])):
            uk_mp3 = "https://dictionary.cambridge.org" + re.search(r'src="(.*)mp3', str(uk[0])).group(0)[5:]
        else:
            uk_mp3 = "None"

        us = soup.find_all('span', class_='us dpron-i')
        us_pron = BeautifulSoup(str(us[0]), features='lxml').get_text()

        if re.search(r'/(.*)/', us_pron):
            us_pron = re.search(r'/(.*)/', us_pron).group(0)
        else:
            us_pron = "No US pronounce"

        if re.search(r'src="(.*)mp3', str(us[0])):
            us_mp3 = "https://dictionary.cambridge.org" + re.search(r'src="(.*)mp3', str(us[0])).group(0)[5:]
        else:
            us_mp3 = "None"

        for block_idx in range(len(word_block)):
            # 词义trans
            word_cy = word_block[block_idx].find_all("div", class_='posgram dpos-g hdib lmr-5')
            word_cy = BeautifulSoup(str(word_cy), features='lxml').text
            block_list.append(word_cy[1:-1])

            # zh and en trans
            zh = word_block[block_idx].find_all("span", class_='trans dtrans dtrans-se break-cj')
            en = word_block[block_idx].find_all("div", class_='def ddef_d db')
            for idx in range(len(en)):
                block_list.append('zh: ' + re.search(r'>(.*)</span>', str(zh[idx])).group(0)[1:-7])
                en_text = BeautifulSoup(str(en[idx]), features='lxml').get_text()
                block_list.append('en: ' + en_text)
                block_list.append('')

            translation_list.append(block_list)
            block_list = []
    else:
        translation_list.append(['search for nothing!'])

    return translation_list, uk_pron, uk_mp3, us_pron, us_mp3
