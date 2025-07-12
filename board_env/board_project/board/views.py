# board/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import F
from django.contrib import messages
from .models import Post, Comment

class PostListView(ListView):
    model = Post
    template_name = 'board/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # 페이지네이션

class PostDetailView(DetailView):
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        # 조회수 증가
        post = super().get_object()
        post.views = F('views') + 1
        post.save(update_fields=['views'])
        post.refresh_from_db()
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comment_set.all()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'board/post_form.html'
    fields = ['title', 'content']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'board/post_form.html'
    fields = ['title', 'content']
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'board/post_confirm_delete.html'
    success_url = reverse_lazy('board:post_list')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# 댓글 관련 뷰
@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, '댓글이 작성되었습니다.')
        else:
            messages.error(request, '댓글 내용을 입력해주세요.')
    return redirect('board:post_detail', pk=pk)

@login_required
def comment_delete(request, pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    post = comment.post
    
    if request.user == comment.author:
        comment.delete()
        messages.success(request, '댓글이 삭제되었습니다.')
    else:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
    
    return redirect('board:post_detail', pk=pk)