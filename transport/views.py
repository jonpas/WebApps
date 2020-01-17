from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django_filters.views import FilterView

from . import models
from . import forms
from . import filters


class TransportListView(LoginRequiredMixin, generic.ListView):
    template_name = 'transport/index.html'
    model = models.Transport

    def get_queryset(self):
        return reversed(self.model.objects.filter(arrived=False).order_by('-id')[:15])  # Last 15 published


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

    def form_valid(self, form):
        # Clear picked and confirmed users when re-opening transport
        if self.object.departed and not form.cleaned_data['departed']:
            self.object.passengers_picked.clear()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'transport/delete.html'
    model = models.Transport
    success_url = reverse_lazy('transport:index')


class TransportReserveView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/passenger.html'
    model = models.Transport
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reserve Transport'
        return context

    def form_valid(self, form):
        self.object.passengers.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportCancelView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/passenger.html'
    model = models.Transport
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cancel Transport'
        return context

    def form_valid(self, form):
        self.object.passengers.remove(self.request.user)
        self.object.passengers_confirmed.remove(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportConfirmView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/passenger.html'
    model = models.Transport
    form_class = forms.TransportConfirmForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Confirm Passengers'
        return context

    def form_valid(self, form):
        for user in form.cleaned_data['passengers']:
            self.object.passengers_confirmed.add(user)
            self.object.passengers.remove(user)
        return http.HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportDepartView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/passenger.html'
    model = models.Transport
    form_class = forms.TransportDepartForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Depart Transport'
        return context

    def form_valid(self, form):
        for user in form.cleaned_data['passengers_confirmed']:
            self.object.passengers_picked.add(user)
        self.object.departed = True
        self.object.save()  # No parent form_valid called to save it
        return http.HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportCompleteView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/passenger.html'
    model = models.Transport
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Complete Transport'
        return context

    def form_valid(self, form):
        self.object.arrived = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class TransportRateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/passenger.html'
    model = models.Transport
    form_class = forms.TransportRateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Rate Transport'
        return context

    def form_valid(self, form):
        ratee_id = self.kwargs['user']

        social = int(form.cleaned_data['social'])
        on_time = int(form.cleaned_data['on_time'])
        luggage = int(form.cleaned_data['luggage'])

        if ratee_id == self.object.carrier.id:
            # Rating carrier
            self.object.carrier.transport_profile.add_rating([social, on_time, luggage])
            self.object.carrier.transport_profile.save()
        else:
            # Rating passenger
            passenger = self.object.passengers_picked.get(id=ratee_id)
            passenger.transport_profile.add_rating([social, on_time, luggage])
            passenger.transport_profile.save()

        self.object.attendees_rated.add(
            User.objects.get(id=ratee_id)
        )
        self.object.save()  # No parent form_valid called to save it

        return http.HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('transport:detail', kwargs={
            'pk': self.object.id,
        })


class ProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'transport/profile_update.html'
    model = models.Profile
    fields = ['carrier', 'passenger']

    def get_success_url(self):
        return reverse_lazy('core:profile', kwargs={
            'pk': self.object.user.id
        })
