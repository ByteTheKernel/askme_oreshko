from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, Tag
from .pagination import paginate
from django.contrib.auth import logout
from django.shortcuts import redirect


def home(request):
    # Получаем все вопросы, отсортированные по дате создания
    questions = Question.objects.new_questions()
    
    # Пагинируем вопросы
    page = paginate(questions, request)
    return render(request, "index.html", {'questions': page.object_list, 'page': page})


def hot_questions(request):
    # Получаем популярные вопросы, отсортированные по количеству лайков
    hot_questions = Question.objects.best_questions()

    # Пагинируем вопросы
    page = paginate(hot_questions, request)
    return render(request, "hot.html", {'hot_questions': page.object_list, 'page': page})


def tag_questions(request, tag_name):
    # Получаем вопросы по тегу
    tag = get_object_or_404(Tag, name=tag_name)  # Получаем тег или 404, если не найден
    tag_questions = Question.objects.questions_by_tag(tag_name)

    # Пагинируем вопросы по тегу
    page = paginate(tag_questions, request)
    return render(request, "tag.html", {'tag': tag_name, 'tag_questions': page.object_list, 'page': page})


def question_detail(request, question_id):
    # Получаем вопрос по ID
    question = get_object_or_404(Question, id=question_id)

    # Получаем ответы на вопрос
    answers = Answer.objects.for_question(question)

    # Пагинируем ответы
    page = paginate(answers, request)

    return render(request, "question_detail.html", {
        'question': question, 
        'answers': page.object_list, 
        'page': page
    })
    

def logout_view(request):
    logout(request)  # Завершаем сессию пользователя
    return redirect('app:home')  # Перенаправляем на главную страницу после выхода


def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')

def settings_view(request):
    return render(request, 'settings.html')


def ask_question(request):
    return render(request, 'ask.html')

