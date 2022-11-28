import random

from django.shortcuts import render
import datetime


def home(request):
    date = datetime.datetime.now().date()
    mood = ['good', 'bad', 'sad', 'happy']
    rage = [i for i in range(20, 31)]
    name = 'tema'
    age = random.choice(rage)
    context = {
        'name': name,
        'age': age,
        'mood': random.choice(mood),
        'date': date
    }
    return render(request, 'home.html', context=context)
