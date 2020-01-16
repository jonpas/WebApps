from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from . import models
from . import forms
from . import filters


class TransportListView(LoginRequiredMixin, generic.ListView):
    template_name = 'transport/index.html'
    model = models.Transport

    def get_queryset(self):
        return reversed(self.model.objects.filter(completed=False).order_by('-id')[:15])  # Last 15 published


class TransportFilterView(LoginRequiredMixin, FilterView):
    template_name = 'transport/search.html'
    model = models.Transport
    filterset_class = filters.TransportFilter


class TransportDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'transport/detail.html'
    model = models.Transport

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except http.Http404:
            return redirect(reverse_lazy('transport:index'))

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class TransportCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'transport/create.html'
    form_class = forms.TransportForm
    model = models.Transport

    def form_valid(self, form):
        form.instance.carrier = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/update.html'
    model = models.Transport
    form_class = forms.TransportForm

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'transport/delete.html'
    model = models.Transport
    success_url = reverse_lazy('transport:index')


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/profile_update.html'
    model = models.Profile
    fields = ['carrier', 'passenger']

    def get_success_url(self):
        return reverse_lazy('core:profile', kwargs={
            'pk': self.object.user.id
        })
