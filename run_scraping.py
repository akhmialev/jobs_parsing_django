import os, sys

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ['DJANGO_SETTINGS_MODULE'] = 'scraping_service.settings'

import django

django.setup()

from src.parsers import work_ua, rabota_ua, djini_co, dou_ua
from scraping.models import Vacancy, City, Language

parsers = (
    dou_ua.main(),
    work_ua.main(),
    djini_co.main(),
    rabota_ua.main(),
)

city = City.objects.filter(slug='kiev')

jobs, errors = [], []

for func in parsers:
    j, e = func
    jobs += j
    errors += e
print(len(jobs))
with open('data.txt', 'w', encoding='utf-8') as file:
    file.write(str(jobs))
