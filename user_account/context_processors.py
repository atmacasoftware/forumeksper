from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from user_account.models import UserProfile


def user_profile(request):
    user_profile = UserProfile.objects.all()
    return dict(user_profile=user_profile)


