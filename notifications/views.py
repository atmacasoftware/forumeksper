from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from notifications.models import Notification


@login_required
def notifications(request):
    notification = Notification.objects.filter(user=request.user)
    return render(request,'pages/notification/notification.html', {'notification':notification})
