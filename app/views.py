from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer, Tag
from .pagination import paginate
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse
from .forms import LoginForm, SignUpForm, ProfileEditForm, QuestionForm, AnswerForm


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
    
    # Создаем пустую форму для отображения
    form = AnswerForm()  

    # Пагинируем ответы
    page = paginate(answers, request)

    return render(request, "question_detail.html", {
        'question': question, 
        'answers': page.object_list, 
        'page': page,
        'form': form,
    })
    

def logout_view(request):
    logout(request)  # Завершаем сессию пользователя
    next_url = request.GET.get('next', 'app:home') # Получаем текущий URL или используем главную страницу по умолчанию
    return redirect(next_url) 


def login_view(request):
    redirect_url = request.GET.get('continue', reverse('app:home'))
    
    if request.user.is_authenticated:
        return redirect(redirect_url)
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect(redirect_url)
    else:
        form = LoginForm()
            
    return render(request, 'login.html', {'form': form, 'continue': redirect_url})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            # Создание нового пользователя
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]                
            )
             
            avatar = form.cleaned_data.get("avatar")
            if avatar:
                user.profile.avatar = avatar
                user.profile.save()
            
             # Логин и редирект на главную страницу
            login(request, user)
            return redirect("app:home")
        
    else:
        form = SignUpForm()   
    
    return render(request, 'signup.html', {'form': form})


@login_required
def settings_view(request):
    user = request.user
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            
            # Сохранение аватара в профиль пользователя
            avatar = request.FILES.get('avatar')
            if avatar:
                user.profile.avatar = avatar
                user.profile.save()
                
            return redirect('app:settings') # Оставляем пользователя на той же странице
    else:
        form = ProfileEditForm(instance=user)
        
    return render(request, 'settings.html', {'form': form, 'user': user})


@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save(commit=True)  # Сохраняем теги и связи ManyToMany
            return redirect('app:question_detail', question_id=question.id)
    else:
        form = QuestionForm()
        
    return render(request, 'ask.html', {'form': form})


@login_required
def add_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            # Перенаправляем с якорем на добавленный ответ
            return redirect(f'/question/{question_id}#answer-{answer.id}')
    else:
        form = AnswerForm()
        
    return redirect('app:question_detail', question_id=question_id)
        