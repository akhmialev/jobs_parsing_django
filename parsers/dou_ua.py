import json

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


# def write_json(datas):
#     with open('dou.json', 'w', encoding='utf-8') as file:
#         json.dump(datas, file, ensure_ascii=False, indent=4)


def get_data(html, errors, url, city=None, language=None):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', attrs={'id': 'vacancyListId'}).find_all('li', class_='l-vacancy')
    datas = []
    if table:
        for element in table:
            title = ' '.join(element.find('div', class_='title').text.strip().split())
            href = element.find('div', class_='title').find('a').get('href')
            company = element.find('div', class_='title').find('a', class_='company').text.strip()
            content = ' '.join(element.find('div', class_='sh-info').text.strip().split())
            # city = element.find('span', class_='cities').text.strip().split(',')

            data = {
                'title': title,
                'url': href,
                'company': company,
                'description': content,
                'city_id': city,
                'language_id': language
            }
            datas.append(data)
        # write_json(datas)
        return datas
    else:
        errors.append({'url': url, 'title': 'Tag does not exist'})


def get_html(url, headers, errors):
    r = requests.get(url, headers=headers)
    if r.ok:
        return r.text
    else:
        errors.append({'url': url, 'title': 'Page do not response'})


def main(url, city=None, language=None):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    errors = []
    html = get_html(url, headers, errors)
    data = get_data(html, url, errors)
    return data, errors

