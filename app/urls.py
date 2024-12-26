from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'app'

urlpatterns = [
    path('', views.home, name='home'),
    path('hot/', views.hot_questions, name='hot'),
    path('tag/<str:tag_name>', views.tag_questions, name='tag'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/add-answer/', views.add_answer, name='add_answer'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('ask/', views.ask_question, name='ask'),
    path('settings/', views.settings_view, name='settings'),
    path('logout/', views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
