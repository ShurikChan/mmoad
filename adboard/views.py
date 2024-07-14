from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import Advertisement


class AdvertisementCreate(CreateView):
    model = Advertisement
    fields = ['title', 'text', 'category', 'video_url', 'image']
    template_name = "adcreate.html"
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IndexView(TemplateView):
    template_name = "index.html"
