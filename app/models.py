from django.db import models
from django.contrib.auth.models import User
from django.db.models import Manager, Q
from django.db.models import Count


# Profile Model - Дополнительный профиль для User
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default_avatar.png', blank=True)
    
    def __str__(self) -> str:
        return f"{self.user.username}'s Profile"
    
    
# Tag Model - Модель тегов для вопросов
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self) -> str:
        return self.name


# Custom Manager for Question Model - для популярных и новых вопросов
class QuestionManager(Manager):
    def best_questions(self):
         # Подсчитываем количество лайков через связку с QuestionLike
        return self.annotate(likes_count=Count('liked_by')).filter(likes_count__gt=0).order_by('-likes_count', '-created_at')

    def new_questions(self):
        return self.order_by('-created_at')
    
    def questions_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name).order_by('-created_at')
    
    
# Question Model - Модель вопросов
class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def likes_count(self):
        return self.liked_by.count()  # Количество лайков для вопроса
    
    def answers_count(self):
        return self.answers.count()

    objects = QuestionManager()  # Используем кастомный менеджер

    def __str__(self):
        return self.title
    
    
class AnswerManager(models.Manager):
    def for_question(self, question):
        return self.filter(question=question).order_by('-created_at')

    
# Answer Model - Модель ответов на вопросы
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def likes_count(self):
        return self.liked_by.count()  # Количество лайков для ответа
    
    objects = AnswerManager() # Используем кастомный менеджер

    def __str__(self):
        return f"Answer by {self.author.username} on {self.question.title}"
    
    
# QuestionLike Model - Лайки для вопросов
class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_likes')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')  # Ограничение на один лайк от пользователя на вопрос

    def __str__(self):
        return f"{self.user.username} liked {self.question.title}"
    

# AnswerLike Model - Лайки для ответов
class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='liked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')  # Ограничение на один лайк от пользователя на ответ

    def __str__(self):
        return f"{self.user.username} liked an answer on {self.answer.question.title}"