from django.db import models
from django.contrib.auth.models import User


class UserCodes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=15, blank=True, null=True)


class Ads_category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=300)
    category = models.ForeignKey(Ads_category, on_delete=models.CASCADE)
    date_in = models.DateTimeField(auto_now_add=True)
    video_url = models.URLField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='static/images')
    responses = models.ManyToManyField(
        User, through='AdReply', related_name='userresponses')

    class Meta:
        ordering = ['-date_in']


class AdReply(models.Model):
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    date_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username} to Ad '{self.advertisement.title}'"
