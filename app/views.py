from django.shortcuts import render
from .pagination import paginate


# Mock data for questions
def generate_mock_questions():
    questions = []
    for i in range(1, 100):
        questions.append({
            'title': f'title {i}',
            'id': i,
            'content': f'text {i}',
            'votes': i,
            'tags': f'xz {i}',
            'answers_count': i+10
        })
    return questions


def home(request):
    questions = generate_mock_questions()
    page = paginate(questions, request)
    return render(request, "index.html", {'questions': page.object_list, 'page': page})


def hot_questions(request):
    hot_questions = generate_mock_questions()
    hot_questions.reverse()
    page = paginate(hot_questions, request)
    return render(request, "hot.html", {'hot_questions': page.object_list, 'page': page})


def tag_questions(request, tag_name):
    tag_questions = generate_mock_questions()
    tag_questions = tag_questions[10:]
    page = paginate(tag_questions, request)
    return render(request, "tag.html", {'tag': tag_name, 'tag_questions': page.object_list, 'page' : page})


def question_detail(request, question_id):
    questions = generate_mock_questions()
    question = questions[question_id]
    
    # Mock data for answers
    answers = [{'content': f'Answer {i}'} for i in range(1, 50)]  # Example answer list
    page = paginate(answers, request)  # Paginate answers
    
    return render(request, "question_detail.html", {
        'question': question, 
        'answers': page.object_list, 
        'page': page
    })
    

def login_view(request):
    return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')

def settings_view(request):
    return render(request, 'settings.html')


def ask_question(request):
    return render(request, 'ask.html')

