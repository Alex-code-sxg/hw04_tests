from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy

from .forms import CreationForm, ChangeForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


class PasswordChange(UpdateView):
    form_class = ChangeForm
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('posts:index')
