# board/admin.py

from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'views', 'get_comment_count']
    list_filter = ['created_at', 'author']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at', 'views']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'author')
        }),
        ('메타데이터', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_comment_count(self, obj):
        return obj.get_comment_count()
    get_comment_count.short_description = '댓글 수'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'post__title']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'content')
        }),
        ('메타데이터', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = '댓글 미리보기'