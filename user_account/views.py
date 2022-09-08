from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, FormView
import json
from forumeksper.settings import EMAIL_HOST_USER
from user_account.forms import SignUpForm
from django.contrib.auth import login, authenticate
# Create your views here.
from user_account.models import UserProfile, UserPoint
from django.contrib.auth.views import LoginView
from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from django.utils.encoding import force_str, DjangoUnicodeDecodeError, force_bytes
from .tokens import account_activation_token
from django.core.mail import EmailMessage


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'pages/register.html')

    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account

        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'pages/register.html', context)

                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                UserProfile.objects.create(user=user, first_name=user.first_name, last_name=user.last_name,
                                           email=user.email)
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                    'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://' + current_site.domain + link
                from_email = EMAIL_HOST_USER
                email = EmailMessage(
                    email_subject,
                    'Merhaba ' + user.username + ', Lütfen aşağıdaki linke tıklayarak hesabınızı aktif ediniz... \n' + activate_url,
                    from_email,
                    [email],
                )
                email.send(fail_silently=False)
                messages.info(request,'Hesabınız oluşturuldu. Aktif etmek için email adresinize gönderilen linki tıklayın. Mail spama düşmüş olabilir.')
                return redirect('login')
            else:
                messages.error(request,
                              'Bu email adresi daha önce kullanılmış!')
                return redirect('register')
        else:
            messages.error(request,
                           'Bu kullanıcı adı daha önce oluşturulmuş!')
            return redirect('register')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Hesabınız aktif edildi. Giriş yapabilirsiniz.')
            return redirect('login')

        except Exception as ex:
            pass

        return redirect('login')


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'pages/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            profile = UserProfile.get_customer_by_username(username=username)
            user = authenticate(username=profile.user, password=password)
            login(request, user)
            error_message = None
            if profile:
                flag = check_password(password, user.password)
                if flag:
                    request.session['user'] = profile.id
                    request.session['email'] = profile.email
                    request.session['first_name'] = profile.first_name
                    request.session['last_name'] = profile.last_name

                    if Login.return_url:
                        return HttpResponseRedirect(Login.return_url)
                    else:
                        Login.return_url = None
                        return redirect('mainpage')
                else:
                    messages.warning(request, 'Email veya şifre hatalı.')

            else:
                messages.warning(request, 'Email veya şifre hatalı.')
                return redirect('login')
            return redirect('login')
        except:
            messages.warning(request, 'Email veya şifre hatalı.')
            return render(request, 'pages/login.html', {'error1': 'Kullanıcı adı veya şifre yanlış olabilir.',
                                                        'error2': 'Hesabınız aktif edilmemiş olabilir. Lütfen email adresini kontrol ediniz. Aktivasyon maili spamlarına düşmüş olabilir.'})



def user_point(request):
    user_point = None
    try:
        user_point = UserPoint.objects.all().order_by('point')[:50]
    except:
        user_point = UserPoint.objects.all().order_by('point')[:50]

    context = {
        'user_point': user_point,
    }

    return render(request, 'pages/user_point.html', context)