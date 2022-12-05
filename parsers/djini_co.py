import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


# def write_json(datas):
#     with open('djini_ua.json', 'w', encoding='utf-8') as file:
#         json.dump(datas, file, ensure_ascii=False, indent=4)


def get_data(html, errors, url):
    domain = 'https://djinni.co'
    soup = BeautifulSoup(html, 'lxml')
    ul = soup.find('ul', class_='list-unstyled list-jobs').find_all('li', class_='list-jobs__item list__item')
    datas = []
    if ul:
        for elemnt in ul:
            title = elemnt.find('a', class_='profile').text.strip()
            href = elemnt.find('a', class_='profile').get('href')
            company = ' '.join(elemnt.find('div', class_='list-jobs__details__info').find('a').text.strip().split())
            content = ' '.join(elemnt.find('div', class_='list-jobs__description').find('p').text.strip().split())
            # city = elemnt.find('span', class_='location-text').text.strip().split(',')[0]
            data = {
                'title': title,
                'url': domain + href,
                'company': company,
                'description': content,
                # 'city': city
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


def main(url):
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    errors = []
    html = get_html(url, headers, errors)
    data = get_data(html, errors, url)
    return data, errors





