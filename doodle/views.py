from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models


class RoomListView(LoginRequiredMixin, generic.ListView):
    template_name = 'doodle/index.html'
    model = models.Room


class RoomCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'room/create.html'
    model = models.Room
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('doodle:room', kwargs={
            'pk': self.object.id,
        })


class RoomDetailView(generic.DetailView):
    template_name = 'room/room.html'
    model = models.Room

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room'] = self.object.name
        return context
