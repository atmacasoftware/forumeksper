from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Notification(models.Model):
    recipient_user = models.ForeignKey(User, related_name="recipient", on_delete=models.CASCADE, verbose_name="Bildirim Gönderilen Kullanıcı" , null=True)
    sender_user = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE, verbose_name="Bildirim Gönderen Kullanıcı",null=True)
    content = models.TextField(verbose_name="Bildirim İçeriği",null=True)
    is_seen = models.BooleanField(default=False,verbose_name="Görüldü Mü?")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    about_notifications = models.CharField(max_length=100, verbose_name="Bildirim Kategorisi", null=True)

    class Meta:
        verbose_name_plural = "Bildirimler"

    def __str__(self):
        return self.sender_user.username + " - " + self.recipient_user.username + " - " + self.about_notifications
