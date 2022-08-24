from django.db import models

# Create your models here.

class Citys(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "1. Şehirler"
        ordering = ('id',)

    def __str__(self):
        return str(self.name)


class WorkType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "2. Çalışma Şekilleri"
        ordering = ('id',)

    def __str__(self):
        return str(self.name)