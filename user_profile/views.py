from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, UpdateView

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