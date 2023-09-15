from django.shortcuts import render, redirect
from django.views import View
from . models import Post
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from . forms import PostCreateUpdateForm
from django.utils.text import slugify
from django.shortcuts import get_object_or_404


class HomeView(View):

    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'home/index.html', {'posts': posts})

    def post(self, request):
        pass



class PostDetailView(View):
    def get(self, request, post_id, post_slug):
        post = get_object_or_404(Post, pk=post_id, slug=post_slug)
        comments = post.post_comments.filter(is_replay=False)

        return render(request, 'home/detail.html', {'post': post, 'comments': comments})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request, 'the post was deleted successfully', 'success')
        else:
            messages.error(request, 'you can not delete this post', 'warning')
        return redirect('home:home_page')


class PostUpdateView(LoginRequiredMixin, View):
    form_class = PostCreateUpdateForm

    def get(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(instance=post)
        return render(request, 'home/update.html', {'form': form})

    def post(self, request, post_id):
        post = Post.objects.get(pk=post_id)
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:20])
            new_post.save()
            messages.success(request, 'post eas updated successfully', 'success')
            return redirect('home:post_detail', post.id, post.slug)


class PostCreateView(View):
    form_class = PostCreateUpdateForm

    def get(self, request):
        form = self.form_class
        return render(request, 'home/create.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.slug = slugify(form.cleaned_data['body'][:20])
            new_post.title = new_post.slug.replace("-", " ")
            new_post.user = request.user
            new_post.save()
            messages.success(request, 'you created new post successfully', 'success')
            return redirect('home:post_detail', new_post.id, new_post.slug)


