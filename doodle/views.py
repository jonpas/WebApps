from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'doodle/index.html'
    model = models.Room


def room(request, room_name):
    return render(request, 'room/room.html', {
        'room': room_name,
    })
