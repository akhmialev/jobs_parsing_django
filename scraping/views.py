from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    vacancy = {}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        vacancy = Vacancy.objects.filter(**_filter)

    title = 'home'
    context = {
        'vacancy': vacancy,
        'title': title,
        'form': form
    }
    return render(request, 'scraping/home.html', context=context)
