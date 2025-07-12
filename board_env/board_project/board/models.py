
# board/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    views = models.PositiveIntegerField(default=0, verbose_name='조회수')

    class Meta:
        ordering = ['-created_at']  # 최신 글부터 정렬
        verbose_name = '게시글'
        verbose_name_plural = '게시글'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:post_detail', kwargs={'pk': self.pk})
    
    def get_comment_count(self):
        return self.comment_set.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='게시글')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    content = models.TextField(verbose_name='댓글 내용')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        ordering = ['created_at']  # 오래된 댓글부터 정렬
        verbose_name = '댓글'
        verbose_name_plural = '댓글'

    def __str__(self):
        return f'{self.post.title} - {self.author.username}'