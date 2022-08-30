from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import datetime
from uuid import uuid4
def create_id():
    now = datetime.datetime.now()
    return str(now.year)+str(now.month)+str(now.day)+str(uuid4())[:7]

# Create your models here.

class RoomCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategori Adı", null=True)
    image = models.ImageField(upload_to='kanal/kategori', null=True, blank=True)
    slug = models.SlugField(unique=True, editable=False)

    class Meta:
        verbose_name_plural = "6. Kategoriler"

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

    def get_category_photos(self):
        if self.image:
            return self.image.url
        else:
            return None

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(RoomCategory, self).save(*args, **kwargs)



class Room(models.Model):
    name = models.CharField(max_length=120, null=True, verbose_name="Kanal Adı")
    slug = models.SlugField(unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Kanal Sahibi")
    category = models.ForeignKey(RoomCategory, on_delete=models.CASCADE, null=True,verbose_name="Kategori Adı")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True, verbose_name="Oluşturulduğu Tarih")
    modified_at = models.DateTimeField(null=True, verbose_name="Güncellendiği Tarih", blank=True)
    image = models.ImageField(upload_to='kanal/kapak', null=True, blank=True)
    banner = models.ImageField(upload_to='kanal/banner', null=True, blank=True)
    description = models.CharField(max_length=160, null=True, verbose_name="Kanal Tanımı", help_text="En fazla 160 karakter")
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

    def get_channel_photos(self):
        if self.image:
            return self.image.url
        else:
            return None

    def get_banner_photos(self):
        if self.banner:
            return self.banner.url
        else:
            return None

    def RoomAdmin(self):
        return self.user.username

    def JoinedRoomAdmin(self,request):
        if self.user.username == request.user.username:
            return True
        else:
            return False

    def RoomManeger(self):
        return self.room_manager.values_list('user__username', flat=True)

    def MemberCount(self):
        return self.member_ship.count()

    def MemberUser(self):
        return self.member_ship.values_list('group_user__username', flat=True)

    def JoinedRoom(self, request):
        if self.member_ship.filter(group_user__username=request.user.username):
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(Room, self).save(*args, **kwargs)



class MemberShip(models.Model):
    group_user = models.ForeignKey(User, related_name="member_ship", on_delete=models.CASCADE, verbose_name="Üye")
    room = models.ForeignKey(Room,related_name="member_ship", on_delete=models.CASCADE, null=True)
    joined_date = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "2. Kanal Üyeleri"

    def __str__(self):
        return self.group_user.username + "-" + self.room.name


class Message(models.Model):
    id = models.CharField(primary_key=True, max_length=255, default=create_id, editable=False)
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE, verbose_name="Kanal Adı")
    user = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE, verbose_name="Kullanıcı")
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    file_type = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ('date_added',)
        verbose_name_plural = "3. Kanal Mesajları"

    def get_username(self):
        return self.user.username

    def __str__(self):
        return self.user.username + " - " + self.room.name


class RoomAnnouncement(models.Model):
    room = models.ForeignKey(Room, related_name="room_announcement", on_delete=models.CASCADE, verbose_name="Kanal Adı")
    user = models.ForeignKey(User, related_name="room_announcement", on_delete=models.CASCADE, verbose_name="Kullanıcı")
    title = models.CharField(max_length=255, verbose_name="Duyuru Başlık", null=True)
    content = models.TextField(verbose_name="Duyuru İçeril")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        ordering = ('date_added',)
        verbose_name_plural = "4. Kanal Duyuruları"

    def __str__(self):
        return self.user.username + " - " + self.room.name + " - " + self.title


class RoomManager(models.Model):
    room = models.ForeignKey(Room, related_name="room_manager", on_delete=models.CASCADE, verbose_name="Kanal")
    user = models.ForeignKey(User, related_name="room_manager", on_delete=models.CASCADE, verbose_name="Kanal Yöneticileri")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Yönetici Olma Tarihi")

    class Meta:
        ordering = ('date_added',)
        verbose_name_plural = "5. Kanal Yöneticileri"

    def __str__(self):
        return self.user.username + " - " + self.room.name

class FavouriteMessage(models.Model):
    room = models.ForeignKey(Room, related_name="favourite_message", on_delete=models.CASCADE, verbose_name="Kanal")
    message = models.ForeignKey(Message, related_name="favourite_message", on_delete=models.CASCADE, verbose_name="Favori Mesaj")
    user = models.ForeignKey(User, related_name="favourite_message", on_delete=models.CASCADE,
                             verbose_name="Favorilere Ekleyen Kullanıcı")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Eklenme Tarihi")

    class Meta:
        ordering = ('date_added',)
        verbose_name_plural = "6. Favori Mesajları"

    def __str__(self):
        return self.user.username + " - " + self.room.name