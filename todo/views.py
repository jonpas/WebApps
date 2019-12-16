from django.shortcuts import render

from . import models


def index(request):
    lists = models.List.objects.order_by('name')
    tasks = models.Task.objects.order_by('name')

    context = {
        'title': 'To-do List',
        'lists': lists,
        'tasks': tasks,
    }
    return render(request, 'todo/index.html', context)
