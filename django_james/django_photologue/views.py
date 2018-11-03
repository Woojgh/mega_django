from django.shortcuts import render
from django.contrib.auth import views as auth_views
from .models import Photo, Album, Project
from django.http import HttpResponseRedirect
from .forms import ProjectUploadForm, EditImageForm
from django.core.urlresolvers import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class add_project_view(View):
    """View used for adding an project to the user."""
    form_class = ProjectUploadForm
    initial = {'form': 'form'}
    template_name = 'projects/add_project.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProjectUploadForm()
        project = Project()
        project.title = request.POST['title']
        project.description = request.POST['description']
        project.image = request.FILES['image']
        project.status = request.POST['status']
        project.save()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse_lazy('projects'), {"form": form})

        return render(request, self.template_name, {'form': form})