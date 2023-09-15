from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=300)
    slug = models.SlugField(unique=True, allow_unicode=True)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created', 'body')

    def __str__(self):
        return f'{self.user} - {self.title}'

    def get_absolute_url(self):
        return reverse('home:post_detail', args=(self.id, self.slug))


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='your_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    replay = models.ForeignKey('self', on_delete=models.CASCADE, related_name='rcomment', blank=True, null=True)
    is_replay = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} -- {self.body[:30]}'

