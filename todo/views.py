from django.views import generic

from . import models


class IndexView(generic.TemplateView):
    template_name = 'todo/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['lists'] = models.List.objects.order_by('name')
        context['tasks'] = models.Task.objects.order_by('name')
        return context
