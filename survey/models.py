from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, Count
from server.models import Room


# Create your models here.

class Survey(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Oda", null=True)
    title = models.CharField(max_length=300, null=True, verbose_name="Anket Sorusu")
    created_user = models.ForeignKey(User, verbose_name="Oluşturan Kullanıcı", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name_plural = "1. Anket"

    def __str__(self):
        return self.created_user.username + "-" + self.title

    def is_answered(self):
        return self.vote_survey.values_list('answered_user__username', flat=True)

    def countVote(self):
        vote = Vote.objects.filter(survey=self, is_answered=True).aggregate(count=Count('id'))
        count = 0
        if vote['count'] is not None:
            count= int(vote['count'])
        return count




class Options(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="option_survey", verbose_name="İlgili Anket", null=True)
    options = models.CharField(max_length=255, null=True, verbose_name="Seçenek")
    options_user = models.ForeignKey(User, verbose_name="Seçenek Oluşturan Kullanıcı", on_delete=models.CASCADE,
                                     null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "2. Anket Seçenekleri"

    def __str__(self):
        return self.options

    def is_answered(self):
        return self.vote_option.values_list('answered_user__username', flat=True)

    def countOptionVote(self):
        vote = Vote.objects.filter(options=self, is_answered=True).aggregate(count=Count('id'))
        count = 0
        if vote['count'] is not None:
            count= int(vote['count'])
        return count

    def rateVate(self):
        full = Vote.objects.filter(survey=self.survey, is_answered=True).aggregate(count=Count('id'))
        vote = Vote.objects.filter(options=self, is_answered=True).aggregate(count=Count('id'))

        result = int((int(vote['count']) * 100)/ (int(full['count'])))

        return result

    def countSurveyVote(self):
        vote = Vote.objects.filter(survey=self.survey, is_answered=True).aggregate(count=Count('id'))
        count = 0
        if vote['count'] is not None:
            count= int(vote['count'])
        return count

class Vote(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="vote_survey",
                               verbose_name="İlgili Anket", null=True)
    options = models.ForeignKey(Options, on_delete=models.CASCADE, related_name="vote_option",
                                verbose_name="Ankete Ait Seçenekler", null=True)
    answered_user = models.ForeignKey(User, verbose_name="Cevap Veren Kullanıcı", related_name="answer_user",
                                      on_delete=models.CASCADE, null=True)
    is_answered = models.BooleanField(default=False, null=True)

    class Meta:
        verbose_name_plural = "3. Anket Cevapları"

    def __str__(self):
        return self.answered_user.username + "-" + self.survey.title + "-" + self.options.options
