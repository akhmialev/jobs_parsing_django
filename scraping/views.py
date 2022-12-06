from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Vacancy
from .forms import FindForm


def home_view(request):
    form = FindForm()

    title = 'home'
    context = {
        'title': title,
        'form': form
    }
    return render(request, 'scraping/home.html', context=context)


def list_view(request):
    form = FindForm()
    city = request.GET.get('city')
    language = request.GET.get('language')
    page_obj = {}
    if city or language:
        _filter = {}
        if city:
            _filter['city__slug'] = city
        if language:
            _filter['language__slug'] = language

        vacancy = Vacancy.objects.filter(**_filter)
        paginator = Paginator(vacancy, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    context = {
        'city': city,
        'language': language,
        'form': form,
        'vacancy': page_obj
    }
    return render(request, 'scraping/list.html', context=context)
