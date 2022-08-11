from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Kanal Adı")
    slug = models.SlugField(unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Kanal Sahibi")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name="Oluşturulduğu Tarih")
    modified_at = models.DateTimeField(null=True, verbose_name="Güncellendiği Tarih", blank=True)
    image = models.ImageField(upload_to='kanal/kapak', null=True, blank=True)
    banner = models.ImageField(upload_to='kanal/banner', null=True, blank=True)
    is_private = models.BooleanField(default=False, null=True, verbose_name="Gizli Mi?")

    class Meta:
        verbose_name_plural = "1. Kanallar"

    def get_slug(self):
        slug = slugify(self.name.replace("ı", "i"))
        unique = slug
        number = 1

        while Room.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(Room, self).save(*args, **kwargs)


class MemberShip(models.Model):
    group_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Üye")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    joined_date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "2. Kanal Üyeleri"

    def __str__(self):
        return self.group_user.username + "-" + self.room.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE, verbose_name="Kanal Adı")
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE, verbose_name="Kullanıcı")
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        ordering = ('date_added',)
        verbose_name_plural = "3. Kanal Mesajları"

    def __str__(self):
        return self.user.username + " - " + self.room.name
