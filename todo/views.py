from django.views import generic
from django.urls import reverse_lazy

from . import models
from . import forms


class IndexView(generic.TemplateView):
    template_name = 'todo/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = models.Tag.objects.order_by('name')
        context['lists'] = models.List.objects.order_by('name')
        context['tasks'] = models.Task.objects.order_by('name')
        return context


class TagCreateView(generic.CreateView):
    template_name = 'todo/create.html'
    model = models.Tag
    fields = '__all__'
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Tag'
        return context


class TagUpdateView(generic.UpdateView):
    template_name = 'todo/update.html'
    model = models.Tag
    fields = '__all__'
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Tag'
        return context


class TagDeleteView(generic.DeleteView):
    template_name = 'todo/delete.html'
    model = models.Tag
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Tag'
        return context


class ListCreateView(generic.CreateView):
    template_name = 'todo/create.html'
    model = models.List
    fields = '__all__'
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New List'
        return context


class ListUpdateView(generic.UpdateView):
    template_name = 'todo/update.html'
    model = models.List
    fields = '__all__'
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit List'
        return context


class ListDeleteView(generic.DeleteView):
    template_name = 'todo/delete.html'
    model = models.List
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete List'
        return context


class TaskCreateView(generic.CreateView):
    template_name = 'todo/create.html'
    form_class = forms.TaskCreateForm
    #model = models.Task
    #fields = '__all__'
    success_url = reverse_lazy('todo:index')

    def get_initial(self, **kwargs):
        initial = super().get_initial(**kwargs)
        initial['list'] = self.kwargs['list']
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Task'
        return context


class TaskUpdateView(generic.UpdateView):
    template_name = 'todo/update.html'
    model = models.Task
    fields = '__all__'
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Task'
        return context


class TaskDeleteView(generic.DeleteView):
    template_name = 'todo/delete.html'
    model = models.Task
    success_url = reverse_lazy('todo:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete Task'
        return context
