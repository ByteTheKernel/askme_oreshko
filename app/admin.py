from django.contrib import admin
from .models import Profile, Tag, Question, Answer, QuestionLike, AnswerLike


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar')
    search_fields = ('user__username',)
    fieldsets = (
        (None, {'fields': ('user', 'avatar')}),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'likes_count')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'content', 'author__username')
    list_editable = ()
    fieldsets = (
        (None, {'fields': ('title', 'content', 'author', 'tags')}),
        ('Additional Info', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at', 'updated_at', 'likes_count')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'question__title')
    list_editable = ()
    fieldsets = (
        (None, {'fields': ('question', 'content', 'author')}),
        ('Additional Info', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'question__title')
    readonly_fields = ('created_at',)


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'answer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'answer__content')
    readonly_fields = ('created_at',)