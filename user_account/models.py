from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
import datetime

from django.utils import timezone

from forumeksper import settings
from mainpage.models import Citys, WorkType


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile', null=True, blank=True)
    bio = models.TextField(max_length=500, null=True)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE, null=True, blank=True)
    service_city = models.ForeignKey(Citys, on_delete=models.CASCADE, null=True, blank=True)
    is_email_activation = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "1. Kullanıcı Hesapları"
    def __str__(self):
        return self.user.username + " " + self.email

    def get_profile_photos(self):
        if self.profile_photo:
            return self.profile_photo.url
        else:
            return None

    @staticmethod
    def get_customer_by_username(username):
        try:
            return UserProfile.objects.get(user__username=username)
        except:
            return False

    def last_seen(self):
        return cache.get('seen_%s' % self.user.username)

    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > self.last_seen() + datetime.timedelta(
                    seconds=settings.USER_ONLINE_TIMEOUT):
                return False
            else:
                return True
        else:
            return False


class UserPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Puan Alan Kullanıcı")
    point = models.PositiveBigIntegerField(verbose_name="Kullanıcı Puanı")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name_plural = "2. Kullanıcı Puanı"

    def __str__(self):
        return self.user.username + " - " + str(self.point)

    def save(self, *args, **kwargs):
        if not self.updated_at:
            self.updated_at = timezone.now()
        super(UserPoint, self).save(*args, **kwargs)
