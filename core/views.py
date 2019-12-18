from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm


class IndexView(generic.TemplateView):
    template_name = 'core/index.html'


class RegisterView(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('core:login')
