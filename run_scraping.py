import asyncio
import os, sys

from django.contrib.auth import get_user_model
from django.db import DatabaseError

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from src.parsers import work_ua, rabota_ua, djini_co, dou_ua
from scraping.models import Vacancy, City, Language, Error, Url

User = get_user_model()

parsers = (
    (dou_ua, 'dou'),
    (work_ua, 'work'),
    (djini_co, 'djini'),
    (rabota_ua, 'rabota'),
)

jobs, errors = [], []


def get_settings():
    qs = User.objects.filter(send_email=True).values()
    settings_lst = set((q['city_id'], q['language_id']) for q in qs)
    return settings_lst


def get_urls(_settings):
    qs = Url.objects.all().values()
    url_dct = {(q['city_id'], q['language_id']): q['url_data'] for q in qs}
    urls = []
    for pair in _settings:
        tmp = {}
        tmp['city'] = pair[0]
        tmp['language'] = pair[1]
        tmp['url_data'] = url_dct[pair]
        urls.append(tmp)
    return urls


async def main(value):
    func, url, city, language = value
    job, err = await loop.run_in_executor(None, func.main, url, city, language)
    errors.extend(err)
    jobs.extend(job)


settings = get_settings()
url_lst = get_urls(settings)

import time

start = time.time()

loop = asyncio.get_event_loop()
tmp_tasks = [(func, data['url_data'][key], data['city'], data['language'])
             for data in url_lst
             for func, key in parsers]

# for data in url_lst:
#     for func, key in parsers:
#         url = data['url_data'][key]
#         j, e = func.main(url, city=data['city'], language=data['language'])
#         jobs += j
#         errors += e

tasks = asyncio.wait([loop.create_task(main(f)) for f in tmp_tasks])
loop.run_until_complete(tasks)
loop.close()
print(time.time() - start)

for job in jobs:
    v = Vacancy(**job)
    try:
        v.save()
    except DatabaseError:
        pass
if errors:
    e = Error(data=errors).save()

with open('data.txt', 'w', encoding='utf-8') as file:
    file.write(str(jobs))
