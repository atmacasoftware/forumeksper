from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.


class ForumCategory(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Forum Kategorisi")
    created_at = models.DateTimeField(editable=False, null=True, auto_now_add=True)
    icon = models.CharField(max_length=100, verbose_name="İkon", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, editable=False)
    status = models.BooleanField(default=True, null=True, )

    class Meta:
        verbose_name_plural = "2. Forum Kategorileri"

    def get_slug(self):
        slug = slugify(self.name.replace("ı", "i"))
        unique = slug
        number = 1

        while ForumCategory.objects.filter(slug=unique).exists():
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
        return super(ForumCategory, self).save(*args, **kwargs)


class Forum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Oluşturan Kullanıcı")
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, verbose_name="Forum Kategorisi", null=True)
    title = models.CharField(max_length=255, verbose_name="Forum Başlığı", null=True)
    content = models.TextField(verbose_name="Forum İçeriği", null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    slug = models.SlugField(unique=True, null=True, editable=False)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "1. Forumlar"

    def get_slug(self):
        slug = slugify(self.title.replace("ı", "i") and self.title.replace("s", "ş"))
        unique = slug
        number = 1

        while Forum.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.forum_comment.count()

    def forumViews(self):
        return self.forum_views.count()

    def isLiked(self):
        return self.like_forum.filter(is_liked=True)

    def isLikedCount(self):
        return self.like_forum.filter(is_liked=True).count()

    def disliked(self):
        return self.dislike_forum.filter(is_liked=True)

    def dislikedCount(self):
        return self.dislike_forum.filter(is_liked=True).count()

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(Forum, self).save(*args, **kwargs)


class ForumComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yorum Yapan Kullanıcı")
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="forum_comment",
                              verbose_name="İlgili Forum")
    content = models.TextField(verbose_name="Yorum", null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "3. Forum Yorumları"

    def __str__(self):
        return self.user.username + " - " + self.forum.title

    def ReplyCommentCount(self):
        return self.forum_reply_comment.count()

    def isLikedComment(self, request):
        return self.like_comment.filter(is_liked=True, user=request.user)

    def isLikedCountComment(self):
        return self.like_comment.filter(is_liked=True).count()

    def dislikedComment(self, request):
        return self.dislike_comment.filter(is_liked=True, user=request.user)

    def dislikedCountComment(self):
        return self.dislike_comment.filter(is_liked=True).count()


class ReplyComment(models.Model):
    forums = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="forum_reply_comment",
                               verbose_name="İlgili Forum")
    comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name="forum_reply_comment",
                                verbose_name="İlgili Yorum")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Yorum Yapan Kullanıcı")
    content = models.TextField(verbose_name="Yorum", null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "4. Yorum Yanıtları"

    def __str__(self):
        return self.user.username + " - " + self.forums.title


class ForumView(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="forum_views")
    ip_address = models.CharField(max_length=100)
    session = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "6. Forum Görüntülenmeleri"

    def __str__(self):
        return self.ip_address + " - " + self.forum.title


class LikeForum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_forum",
                             verbose_name="Beğenen Kullanıcı")
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="like_forum", verbose_name="İlgili Forum")
    ip = models.CharField(max_length=20, blank=True)
    is_liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "5.1 Forum Beğenmeleri"

    def __str__(self):
        return self.user.username + " - " + self.forum.title


class DisLikeForum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dislike_forum",
                             verbose_name="Beğenmeyen Kullanıcı")
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="dislike_forum",
                              verbose_name="İlgili Forum")
    ip = models.CharField(max_length=20, blank=True)
    is_liked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "5.2 Forum Beğenmemeleri"

    def __str__(self):
        return self.user.username + " - " + self.forum.title


class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_comment",
                             verbose_name="Beğenen Kullanıcı")
    comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name="like_comment",
                                verbose_name="İlgili Forum")
    ip = models.CharField(max_length=20, blank=True, null=True)
    is_liked = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "5.3 Yorum Beğenmeleri"

    def __str__(self):
        return self.user.username


class DisLikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dislike_comment",
                             verbose_name="Beğenmeyen Kullanıcı")
    comment = models.ForeignKey(ForumComment, on_delete=models.CASCADE, related_name="dislike_comment",
                                verbose_name="İlgili Forum")
    ip = models.CharField(max_length=20, blank=True, null=True)
    is_liked = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "5.4 Forum Beğenmemeleri"

    def __str__(self):
        return self.user.username


class EditorSelectForum(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, verbose_name="Seçilecek Forum")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=False, verbose_name="Gösterilsin mi?")

    class Meta:
        verbose_name_plural = "7. Editör Seçimi"

    def __str__(self):
        return self.forum.title


class UserForumPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Puan Alan Kullanıcı")
    point = models.PositiveBigIntegerField(verbose_name="Kullanıcı Puanı")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "8. Kullanıcı Puanı"

    def __str__(self):
        return self.user.username + " - " + self.point
