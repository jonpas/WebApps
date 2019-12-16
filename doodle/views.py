from django.shortcuts import render


def index(request):
    return render(request, 'doodle/index.html', {
        'title': 'Doodle (game)',
    })
