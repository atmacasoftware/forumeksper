from django.contrib.auth.models import User
from django.db import models

from server.models import Room


# Create your models here.

class Survey(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Oda", null=True)
    title = models.CharField(max_length=300, null=True, verbose_name="Anket Sorusu")
    created_user = models.ForeignKey(User, verbose_name="Oluşturan Kullanıcı", on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,null=True)

    class Meta:
        verbose_name_plural = "1. Anket"

    def __str__(self):
        return self.created_user.username + "-" + self.title


class Options(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="İlgili Anket", null=True)
    options = models.CharField(max_length=255, null=True, verbose_name="Seçenek")
    options_user = models.ForeignKey(User, verbose_name="Seçenek Oluşturan Kullanıcı", on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=False,null=True)

    class Meta:
        verbose_name_plural = "2. Anket Seçenekleri"

    def __str__(self):
        return self.options


class Vote(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name="İlgili Anket", null=True)
    options = models.ForeignKey(Options,on_delete=models.CASCADE, verbose_name="Ankete Ait Seçenekler", null=True)
    answered_user = models.ForeignKey(User, verbose_name="Cevap Veren Kullanıcı", on_delete=models.CASCADE, null=True)
    is_answered = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name_plural = "3. Anket Cevapları"

    def __str__(self):
        return self.answered_user.username + "-" + self.survey.title + "-" + self.options.options
