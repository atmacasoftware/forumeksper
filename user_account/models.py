from django.contrib.auth.models import User
from django.db import models
from django.core.cache import cache
import datetime
from forumeksper import settings


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    profile_photo = models.ImageField(upload_to='profile', null=True, blank=True)
    is_email_activation = models.BooleanField(default=False)


    class Meta:
        verbose_name_plural = "1. Kullanıcı Hesapları"
    def __str__(self):
        return self.user.username + " " + self.email

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