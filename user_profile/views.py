from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic.edit import UpdateView

from user_profile.forms import PasswordChangeCustomForm, UpdateProfilePhotoForm
from user_profile.models import UserProfile

from django.contrib.auth import logout


@login_required
def logout_view(request):
    logout(request)
    return redirect('blog')


@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.pk)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == 'POST':
        form = UpdateProfilePhotoForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile')

    else:
        form = UpdateProfilePhotoForm(instance=request.user)

    return render(request, 'user_profile/user_profile.html', {'form': form, 'user': user_profile})


class UserProfileEdit(LoginRequiredMixin, UpdateView):
    fields = ('username', 'email', 'first_name', 'last_name')
    template_name = 'user_profile/user_profile_edit.html'

    def get_object(self, **kwargs):
        return self.request.user

    def get_success_url(self, **kwargs):
        return reverse('user_profile')

    def form_valid(self, form):
        email = form.cleaned_data['email']

        if email:

            try:
                user = User.objects.get(email=email)
            except Exception:
                user = None

            if user:
                messages.error(self.request, 'Пользователь с таким электронным адресом уже существует')
                return redirect('user_profile_edit')

            protocol = 'http://'
            domain = get_current_site(self.request).domain
            uidb64 =urlsafe_base64_encode(force_bytes(self.request.user.pk))
            token = default_token_generator.make_token(self.request.user)
            url = f'{protocol}{domain}/profile/verify_email/{uidb64}/{token}'
            mail = send_mail('Подтверждение Email', f'Ссылка для подтверждения: {url}', 'your email', [email])
            if mail:
                messages.success(self.request, 'На вашу почту отправлено письмо с подтверждением')
        else:
            self.request.user.profile.email_verify = False
            self.request.user.profile.save()
        return super().form_valid(form)


class VerifyEmail(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist, ValidationError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.profile.email_verify = True
            user.profile.save()
            messages.success(self.request, 'Ваша почта успешно подтверждена')
            return redirect('user_profile')

        return redirect('verify_error')


def verify_error(request):
    return render(request, 'user_profile/verify_error.html')


class UserPersonalDataEdit(LoginRequiredMixin, UpdateView):
    fields = ('country', 'city', 'tel')
    template_name = 'user_profile/user_personal_data_edit.html'

    def get_object(self, **kwargs):
        return UserProfile.objects.get(user=self.request.user)

    def get_success_url(self, **kwargs):
        return reverse('user_profile')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeCustomForm
    template_name = 'user_profile/user_profile_edit.html'
    success_url = reverse_lazy("user_profile")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = User.objects.get(pk=self.request.user.pk)
        return kwargs

    def get_success_url(self, **kwargs):
        return reverse('user_profile')