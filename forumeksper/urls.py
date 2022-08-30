"""forumeksper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.views.static import serve
from django.conf import settings

from mainpage.views import mainpage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_account.urls')),
    path('', include('mainpage.urls')),
    path('server/', include('server.urls')),
    path('survey/', include('survey.urls')),
    path('forum/', include('forums.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = 'mainpage.views.error_404'
handler500 = 'mainpage.views.error_500'

admin.site.site_title = 'Forum Eksper Yönetimi'
admin.site.site_header = 'Forum Eksper Yönetim Paneli'
admin.site.index_title = 'Forum Eksper Yönetimi Paneline Hoş Geldiniz'