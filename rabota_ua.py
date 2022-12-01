import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def write_json(datas):
    with open('rabota.json', 'w', encoding='utf-8') as file:
        json.dump(datas, file, ensure_ascii=False, indent=4)


def get_data(html, url, errors):
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_='serp-item')
    datas = []
    if cards:
        for card in cards:
            title = card.find('a', class_='serp-item__title').text.strip()
            href = card.find('a', class_='serp-item__title').get('href')
            company = ' '.join(card.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text.strip().split())
            content = ''
            city = ' '.join(card.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text.strip().split())
            data = {
                'title': title,
                'href': href,
                'company': company,
                'content': content,
                'city': city
            }
            datas.append(data)
        write_json(datas)
        return datas
    else:
        errors.append({'url': url, 'title': 'Tag does not exist'})


def get_html(url, headers, errors):
    response = requests.get(url, headers=headers)
    if response.ok:
        return response.text
    else:
        errors.append({'url': url, 'title': 'Page do not response'})


def main():
    url = 'https://rabota.by/search/vacancy?text=python'
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    errors = []
    html = get_html(url, headers, errors)
    data = get_data(html, url, errors)
    print(errors)


if __name__ == '__main__':
    main()
