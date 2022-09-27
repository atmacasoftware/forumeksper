from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
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

class BankList(models.Model):
    name = models.CharField(max_length=150, verbose_name="Banka İsmi", null=True)
    slug = models.SlugField(unique=True, null=True, editable=False)
    logo = models.ImageField(upload_to='banka/logo', null=True, blank=True, verbose_name="Banka Logosu")
    created_at = models.DateTimeField(editable=False, null=True, auto_now_add=True)
    is_important = models.BooleanField(default=False, null=True, verbose_name="Anasayfada Gösterilsin Mi?")

    class Meta:
        verbose_name_plural = "3. Banka İsimleri"

    def __str__(self):
        return self.name

    def get_slug(self):
        slug = slugify(self.name.replace("ı", "i"))
        unique = slug
        number = 1

        while BankList.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(BankList, self).save(*args, **kwargs)


class LoanInterestRate(models.Model):

    STATES = (
        ('Arttı','Arttı'),
        ('Azaldı','Azaldı'),
        ('Stabil','Stabil'),
    )

    bank = models.ForeignKey(BankList, on_delete=models.CASCADE, related_name='rate_bank', null=True, verbose_name="Banka Adı")
    rate = models.FloatField(default=0.0, verbose_name="Kredi Oranı")
    state = models.CharField(choices=STATES, verbose_name="Durum", max_length=50)
    created_at = models.DateTimeField(editable=False, null=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = "4. Kredi Faiz Oranları"

    def __str__(self):
        return self.bank.name + " - " + str(self.rate)


class Weather(models.Model):
    city = models.ForeignKey(Citys, on_delete=models.CASCADE, verbose_name="Şehir", default=6)
    ip = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = "5. Şehir Hava Durumu"

    def __str__(self):
        return self.city.name


class NewsCategory(models.Model):
    name = models.CharField(verbose_name="Haber Kategorisi", max_length=150, null=True)
    slug = models.SlugField(unique=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "6. Haber Kategorileri"

    def __str__(self):
        return self.name

    def get_slug(self):
        slug = slugify(self.name.replace("ı", "i"))
        unique = slug
        number = 1

        while NewsCategory.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        self.slug = self.get_slug()
        return super(NewsCategory, self).save(*args, **kwargs)


class AdsCategory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategori Adı")
    price = models.DecimalField(decimal_places=2, max_digits=20, default=1.0,verbose_name="Fiyat")
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    update_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, null=True, editable=False)

    class Meta:
        verbose_name_plural = "7.1. Reklam Kategorileri"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_slug(self):
        slug = slugify(self.name.replace("ı", "i"))
        unique = slug
        number = 1

        while AdsCategory.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(AdsCategory, self).save(*args, **kwargs)


class AdvertisementType(models.Model):
    name = models.CharField(max_length=255, verbose_name="Kategori Adı")
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    update_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, null=True, editable=False)

    class Meta:
        verbose_name_plural = "7.2. İlan Kategorileri"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_slug(self):
        slug = slugify(self.name.replace("ı", "i"))
        unique = slug
        number = 1

        while AdvertisementType.objects.filter(slug=unique).exists():
            unique = '{}-{}'.format(slug, number)
            number += 1

        return unique

    def save(self, *args, **kwargs):
        self.slug = self.get_slug()
        return super(AdvertisementType, self).save(*args, **kwargs)


class Advertisement(models.Model):

    first_name = models.CharField(max_length=100, verbose_name="İsim", null=True)
    last_name = models.CharField(max_length=100, verbose_name="Soyisim", null=True)
    company = models.CharField(max_length=100, verbose_name="Şirket Adı", null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, verbose_name="Email")
    phone = models.CharField(max_length=11, verbose_name="Telefon", null=True)
    type = models.ForeignKey(AdvertisementType, on_delete=models.CASCADE, null=True, verbose_name="İlan Tipi")
    ads = models.ForeignKey(AdsCategory, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Reklam Kategorisi")
    title = models.CharField(max_length=120, verbose_name="Haber Başlığı", null=True, blank=True)
    message = models.TextField(verbose_name="Mesaj", null=True)
    is_private = models.BooleanField(default=False, null=True)
    image = models.ImageField(upload_to='ilan/', null=True, blank=True, verbose_name="İlan Resimleri")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)

    class Meta:
        verbose_name_plural = "7. İlanlar"

    def __str__(self):
        return self.first_name + " " + self.last_name + " " + self.email


class Note(models.Model):
    PAGES = (
        ('1','Anasayfa'),
        ('2','İlan'),
    )

    pages = models.CharField(choices=PAGES, max_length=100, null=True, verbose_name="Sayfa Seçimi")
    content = models.TextField(verbose_name="İçerik", null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name_plural = "8. Notlar"





