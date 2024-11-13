from django.urls import path
from app import views


app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag_name>', views.tag_questions, name='tag'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('ask/', views.ask_question, name='ask'),
    path('settings/', views.settings_view, name='settings'),
    
]
