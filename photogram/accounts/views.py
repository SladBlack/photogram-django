from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, FormView

from .forms import UpdateForm, CreateUserForm


class SignUpView(CreateView):
    """Регистрация"""
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UsersList(LoginRequiredMixin, ListView):
    """Список пользователей"""
    model = User
    template_name = 'accounts/accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class CreateUser(LoginRequiredMixin, CreateView):
    """Создание пользователя"""
    form_class = CreateUserForm
    success_url = reverse_lazy('user_list')
    template_name = 'accounts/create_user.html'


class DeleteUser(LoginRequiredMixin, DeleteView):
    """Удаление пользователя"""
    model = User
    success_url = reverse_lazy('user_list')
    template_name = 'accounts/delete_confirm.html'


class BlockUser(LoginRequiredMixin, FormView):
    """Блокирование/разблокирование пользователя"""
    model = User
    template_name = 'accounts/accounts.html'
    success_url = reverse_lazy('posts')
    form_class = UpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.request.POST.get('id'))
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        context['users'] = User.objects.all()
        return context


