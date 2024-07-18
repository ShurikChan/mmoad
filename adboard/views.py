from typing import Any
from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, View, DeleteView
from .models import Advertisement, AdReply, UserCodes
from .forms import AdReplyForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from mmoad.settings import EMAIL_HOST_USER
from django.contrib.auth.mixins import LoginRequiredMixin


class AdvertisementCreate(LoginRequiredMixin, CreateView):
    model = Advertisement
    fields = ['title', 'text', 'category', 'video_url', 'image']
    template_name = "adcreate.html"
    success_url = '/adlist'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IndexView(TemplateView):
    template_name = "index.html"


class AdvertisementView(ListView):
    model = Advertisement
    template_name = "adlist.html"
    context_object_name = 'ad'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ads'] = Advertisement.objects.all()
        context['form'] = AdReplyForm()
        return context


class AdvertisementDetail(DetailView):
    model = Advertisement
    template_name = "addetail.html"
    context_object_name = 'ad'


class AdvertisementUpdate(LoginRequiredMixin, UpdateView):
    model = Advertisement
    fields = ['title', 'text', 'category', 'video_url', 'image']
    template_name = "adedit.html"
    success_url = '/adlist'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ad_author'] = Advertisement.objects.get(pk=self.kwargs.get('pk')).user
        return context


class ProfileView(LoginRequiredMixin, TemplateView):
    model = Advertisement
    template_name = "profile.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['ads'] = Advertisement.objects.all().filter(
            user=self.request.user)
        return context


class DoResponse(LoginRequiredMixin, View):
    def post(self, request, pk):
        form = AdReplyForm(request.POST)
        if form.is_valid():
            ad_reply = form.save(commit=False)
            ad_reply.user = request.user
            ad_reply.advertisement_id = pk
            ad_reply.save()
            # Send email to ad author about new response
            ad = Advertisement.objects.get(pk=pk)
            ad_author_email = ad.user.email
            subject = 'New response to your advertisement'
            message = f'User {request.user.username} has replied to your advertisement: {ad.title}'
            from_email = EMAIL_HOST_USER
            recipient_list = [ad_author_email]
            send_mail(subject, message, from_email, recipient_list)
            # email has been sent
            return HttpResponseRedirect('/adlist')
        

class AdResponsesView(LoginRequiredMixin, DetailView):
    model = Advertisement
    template_name = "adresponses.html"
    context_object_name = 'ads'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        ad_id = self.kwargs['pk']
        context['responses'] = AdReply.objects.filter(advertisement_id=ad_id)
        context['ad_author'] = Advertisement.objects.get(pk=self.kwargs.get('pk')).user
        return context
    
class AdvertisementDelete(LoginRequiredMixin, DeleteView):
    model = Advertisement
    template_name = "addelete.html"
    success_url = '/accounts/profile'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['ad'] = Advertisement.objects.get(pk=self.kwargs['pk'])
        context['ad_author'] = Advertisement.objects.get(pk=self.kwargs.get('pk')).user
        return context
    

class AdResponseDelete(LoginRequiredMixin, View):
    def post(self, request, pk):
        response = AdReply.objects.get(pk=pk)
        response.delete()
        return redirect(request.META.get('HTTP_REFERER'))


class ConfirmUser(UpdateView):
    model = UserCodes
    context_object_name = 'confirm_user'

    def post(self, request, *args, **kwargs):
        if 'code' in request.POST:
            code = UserCodes.objects.filter(code=request.POST['code'])
            if code.exists():
                user = code[0].user
                user.is_active = True
                user.save()
                code.delete()
            else:
                return render(self.request, 'users/invalid_code.html')
            return redirect('account_login')
        

class AcceptResponse(LoginRequiredMixin, View):
    def post(self, request, pk):
        response = AdReply.objects.get(pk=pk)
        user_email = response.user.email
        send_mail(
            'Response Accepted',
            f'Your response to the advertisement: {response.advertisement.title} has been accepted.',
            EMAIL_HOST_USER,
            [user_email],
        )
        return redirect(request.META.get('HTTP_REFERER'))