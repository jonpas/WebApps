from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin

from . import models


class RoomListView(LoginRequiredMixin, generic.ListView):
    template_name = 'doodle/index.html'
    model = models.Room


class RoomDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'doodle/room.html'
    model = models.Room

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except http.Http404:
            return redirect(reverse_lazy('doodle:index'))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class RoomCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'doodle/create.html'
    model = models.Room
    fields = ['name']

    def get_success_url(self):
        return reverse_lazy('doodle:room', kwargs={
            'pk': self.object.id,
        })


class RoomDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'doodle/delete.html'
    model = models.Room
    success_url = reverse_lazy('doodle:index')
