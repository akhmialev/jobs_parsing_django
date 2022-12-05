import json

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


#
# def write_json(data):
#     with open('work.json', 'w', encoding='utf-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=4)


def get_data(html, url, errors):
    domain = 'https://www.work.ua'
    soup = BeautifulSoup(html, 'lxml')
    cards = soup.find_all('div', class_='card card-hover card-visited wordwrap job-link')
    datas = []
    if cards:
        for card in cards:
            title = card.find('h2').text.strip()
            href = card.find('h2').find('a').get('href')
            company = card.find('div', class_='add-top-xs').find('span').text.strip()
            content = ' '.join(card.find('p', class_='overflow text-muted add-top-sm cut-bottom').text.strip().split())
            # city = ' '.join(
            #     card.find('div', class_="add-top-xs").find('span', class_='middot').next.text.strip().split())

            data = {
                'title': title,
                'url': domain + href,
                'description': content,
                'company': company,
                # 'city': city
            }
            datas.append(data)
        # write_json(datas)
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
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    url = 'https://www.work.ua/jobs-kyiv-python/'
    errors = []
    html = get_html(url, headers, errors)
    data = get_data(html, url, errors)
    return data, errors


if __name__ == '__main__':
    main()
