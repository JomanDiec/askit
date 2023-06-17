from django.urls import include, path
from django.urls import re_path as url
from . import views
from .views import HomePageView

app_name = 'ask_it'

urlpatterns = [
  path('test_page', views.test_page, name='test_page'),
  path("image_test", HomePageView.as_view(), name="test"),
  path('test', views.test, name='test'),
  path('home', views.home, name='home'),
  path('latest_sort', views.latest_sort, name='latest_sort'),
  path('ask_login', views.ask_login, name='ask_login'),
  path('ask_login_form', views.ask_login_form, name='ask_login_form'),
  path('registration', views.registration, name='registration'),
  path('registration_form', views.registration_form, name='registration_form'),
  path('question', views.question, name='question'),
  path('question_form', views.question_form, name='question_form'),
  path('question_thread/<int:question_thread_id>', views.question_thread, name='question_thread'),
  path('question_delete/<int:question_id>', views.question_delete, name='question_delete'),
  path('reply_delete/<int:reply_id>', views.reply_delete, name='reply_delete'),
  path('upvote/<int:question_id>', views.upvote, name='upvote'),
  path('upvote_reply/<int:reply_id>', views.upvote_reply, name='upvote_reply'),
  path('give_cookie/<int:receiver_id>', views.give_cookie, name='give_cookie'),
  path('give_reply_cookie/<int:receiver_id>', views.give_reply_cookie, name='give_reply_cookie'),
  path('thread_reply/<int:question_thread_id>', views.thread_reply, name='thread_reply'),
  path('change_password', views.change_password, name='change_password'),
  path('change_password_form', views.change_password_form, name='change_password_form'),
  path('ask_logout', views.ask_logout, name='ask_logout'),
]