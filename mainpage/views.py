from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from notifications.models import Notification
from user_account.models import UserProfile

def mainpage(request):
    profile = UserProfile.objects.all()
    person_profile = None
    notification = None
    notification_count = None
    if request.user.is_authenticated:
        person_profile = UserProfile.objects.get(user=request.user)
        notification = Notification.objects.filter(recipient_user=request.user)
        notification_count = Notification.objects.filter(recipient_user=request.user).count()
    return render(request,'pages/mainpage.html',{'profile':profile,'person_profile':person_profile,'notification':notification,'notification_count':notification_count})
