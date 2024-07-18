from django import forms
from .models import AdReply, UserCodes
from allauth.account.forms import SignupForm
import random
from string import hexdigits
from django.core.mail import send_mail
from mmoad.settings import EMAIL_HOST_USER

class AdReplyForm(forms.ModelForm):
    class Meta:
        model = AdReply
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1, 'cols': 40, 'placeholder': 'type your ad reply'}),
        }
        labels = {
            'text': ''}

class CommonSignUpForm(SignupForm):
    def save(self, request):
        user = super(CommonSignUpForm, self).save(request)
        user.is_active = False
        user.save()
        code = ''.join(random.sample(hexdigits, 5))
        user_with_code = UserCodes.objects.create(user=user, code=code)
        user_with_code.save()
        send_mail(
            subject="Activation code",
            message=f"Your activation code is: {code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return user