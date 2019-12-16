from django.shortcuts import render


def index(request):
    return render(request, 'transport/index.html', {
        'title': 'Transporter',
    })
