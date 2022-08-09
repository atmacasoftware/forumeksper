from django.shortcuts import render

# Create your views here.
from user_account.models import UserProfile


def mainpage(request):
    profile = UserProfile.objects.all()
    return render(request,'pages/mainpage.html',{'profile':profile})