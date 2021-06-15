from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post
from .forms import PostForm


class PostsView(FormView, ListView):
    """Лента постов"""
    model = Post
    paginate_by = 4
    form_class = PostForm
    template_name = 'home.html'
    success_url = reverse_lazy('posts')

    def get_queryset(self):
        query = Post.objects.all().order_by('id').reverse()
        return query

    def form_valid(self, form):
        for item in self.request.FILES.getlist('image'):
            Post.objects.create(image=item, author=self.request.user, tag=form.clean()['tag'])
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, DetailView):
    """Страница с отдельным постом"""
    model = Post
    template_name = 'posts/post_detail.html'

    def get_object(self):
        post = super().get_object()
        post.view_count += 1
        post.save()

        self.view_count = post.view_count
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_count'] = self.view_count
        return context


class DeletePost(LoginRequiredMixin, DeleteView):
    """Удаление поста"""
    model = Post
    success_url = reverse_lazy('posts')

    def get_object(self, queryset=None):
        post = super(DeletePost, self).get_object()
        if not post.author == self.request.user:
            raise Http404
        return post


class UpdatePost(LoginRequiredMixin, UpdateView):
    """Редактирование поста"""
    model = Post
    fields = ['image', 'tag']
    template_name_suffix = '_update'


class FilterView(ListView, FormView):
    """Фильтрация постов по тегу"""
    model = Post
    template_name = 'home.html'
    form_class = PostForm
    success_url = reverse_lazy('posts')
    template_name_suffix = 'page_obj'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = Post.objects.filter(tag=self.request.GET.get('tag')).order_by('id').reverse()
        return context


class MyPostsView(ListView, FormView):
    model = Post
    template_name = 'home.html'
    template_name_suffix = 'page_obj'
    form_class = PostForm
    success_url = reverse_lazy('posts')
    paginate_by = 4

    def get_queryset(self):
        query = Post.objects.filter(author=self.request.user).order_by('id').reverse()
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_obj'] = Post.objects.filter(author=self.request.user).order_by('id').reverse()
        return context
