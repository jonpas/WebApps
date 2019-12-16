from django.shortcuts import render


def index(request):
    return render(request, 'ludo/index.html', {
        'title': 'Ludo (game)',
    })
