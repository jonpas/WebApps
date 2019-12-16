from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html', {
        'title': 'Web Apps',
        'pages': [
            {
                'url': '/todo/',
                'title': 'To-do List',
            },
        ],
    })
