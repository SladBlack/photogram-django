from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, DeleteView

from .models import Post
from .forms import PostForm


class PostsView(FormView):
    """Лента постов"""
    model = Post
    form_class = PostForm
    template_name = 'home.html'
    success_url = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Post.objects.all().order_by('id').reverse()
        return context

    def form_valid(self, form):
        for item in self.request.FILES.getlist('image'):
            Post.objects.create(image=item, author=self.request.user)
        return super().form_valid(form)


class PostDetailView(DeleteView):
    """Страница с отельным постом"""
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


class DeletePost(DeleteView):
    """Удаление поста"""
    model = Post
    success_url = reverse_lazy('posts')

    def get_object(self, queryset=None):
        post = super(DeletePost, self).get_object()
        if not post.author == self.request.user:
            raise Http404
        return post
