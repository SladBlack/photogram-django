from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class UsersList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/accounts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context


class DeleteUser(LoginRequiredMixin, DeleteView):
    """Удаление пользователя"""
    model = User
    success_url = reverse_lazy('user_list')
    template_name = 'accounts/delete_confirm.html'
