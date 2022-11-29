from django.shortcuts import render
from .models import Vacancy
import datetime


def home_view(request):
    vacancy = Vacancy.objects.all()
    title = 'home'
    date = datetime.datetime.now()
    context = {
        'vacancy': vacancy,
        'title': title,
        'date': date
    }
    return render(request, 'scraping/home.html', context=context)
