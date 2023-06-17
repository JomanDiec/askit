from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
# from exercises.models import *
from ask_it.models import *
from django.db.models.functions import Lower
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator
import os

def test_page(request):
  return HttpResponse("Bingo!")

def test(request):
  images = QuestionImage.objects.all()

  context = {"author": "gaurav singhal", 'images' : images}
  return render(request, 'ask_it/bootstrap_template.html', context)

# not being used
class HomePageView(ListView):
    model = QuestionImage
    template_name = "test.html"

def home(request):
  sort = request.GET.get('sort')
  size = Ask_it.objects.count()
  posts = Ask_it.objects.order_by('-id')
  search = ''
  # thread = Reply.objects.filter(parent=question_thread_id)
  if 'search_term' in request.GET:
    questions = Ask_it.objects.filter(Q(question__icontains=request.GET['search_term'].strip()) | Q(message__icontains=request.GET['search_term'].strip())).order_by('-created_at')
    search = request.GET['search_term'].strip()
  elif sort == 'oldest':
    questions = Ask_it.objects.order_by('created_at')
  elif sort == 'popular':
    questions = Ask_it.objects.order_by('-upvotes')
  else:
    questions = Ask_it.objects.all().order_by('-created_at')

  paginator = Paginator(questions, 4)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  
  context = { 'questions' : questions , 'size' : size , posts : 'posts' , 'page_obj': page_obj, 'search' : search, 'sort' : sort}
  return render(request, 'ask_it/home.html', context, )

@login_required
def question_delete(request, question_id):
  question = Ask_it.objects.get(id=question_id)
  if request.user == question.author:
    if question.image:
      os.remove(question.image.path)
    question.delete()
  else:
    HttpResponse('you are not the author') #should not be accessible

  return HttpResponseRedirect(reverse('ask_it:home'))

@login_required
def reply_delete(request, reply_id):
  reply = Reply.objects.get(id=reply_id)
  if request.user == reply.author:
    reply.delete()
  else:
    HttpResponse('you are not the author') #should not be accessible
    
  next = request.GET.get('next', '/home')
  return HttpResponseRedirect(next)

def upvote(request, question_id):
  user = request.user
  if user.is_authenticated:
    question = Ask_it.objects.get(id=question_id)
    upvote_check = Upvoted.objects.filter(user=user,upvoted_questions=question).exists()
    if upvote_check == False:
      question.upvotes += 1
      Upvoted.objects.create(user=user, upvoted_questions=question)
      question.save()
      next = request.GET.get('next', '/home')
      return HttpResponseRedirect(next) #returns to current page
    else:
      question.upvotes -= 1
      Upvoted.objects.filter(user=user, upvoted_questions=question).delete()
      question.save()
      next = request.GET.get('next', '/home')
      return HttpResponseRedirect(next) #returns to current page
  else:
    return HttpResponseRedirect(reverse('ask_it:ask_login'))

def upvote_reply(request, reply_id):
  user = request.user
  if user.is_authenticated:
    reply = Reply.objects.get(id=reply_id)
    upvote_check = Upvoted.objects.filter(user=user,upvoted_reply=reply).exists()
    if upvote_check == False:
      reply.upvotes += 1
      Upvoted.objects.create(user=user, upvoted_reply=reply)
      reply.save()
      next = request.GET.get('next', '/home')
      return HttpResponseRedirect(next)
    else:
      reply.upvotes -= 1
      Upvoted.objects.filter(user=user, upvoted_reply=reply).delete()
      reply.save()
      next = request.GET.get('next', '/home')
      return HttpResponseRedirect(next)
  else:
    return HttpResponseRedirect(reverse('ask_it:ask_login'))

@login_required
def give_cookie(request, receiver_id):
  user = request.user
  cookie_jar = Cookie_jar.objects.get(user=user) #cookie jar of user
  receiver = Ask_it.objects.get(id=receiver_id) #ask_it post receiving cookie
  if cookie_jar.cookies > 0:
    cookie_jar.cookies -= 1
    receiver.cookies += 1
    receiver.author.cookie_jar.cookies += 1 #cookie jar of author of post
    cookie_jar.save()
    receiver.save()
    receiver.author.cookie_jar.save()
    
    next = request.GET.get('next', '/home')
    return HttpResponseRedirect(next) #direct to current page
  else:
    return HttpResponse('you dont have any cookies, you should not be here!') #should not be accessible

@login_required
def give_reply_cookie(request, receiver_id):
  user = request.user
  cookie_jar = Cookie_jar.objects.get(user=user)
  receiver = Reply.objects.get(id=receiver_id)
  if cookie_jar.cookies > 0:
    cookie_jar.cookies -= 1
    receiver.cookies += 1
    receiver.author.cookie_jar.cookies += 1
    cookie_jar.save()
    receiver.save()
    receiver.author.cookie_jar.save()
    
    next = request.GET.get('next', '/home')
    return HttpResponseRedirect(next)
  else:
    return HttpResponse('you dont have any cookies, you should not be here!')

# alternate function to above (not currently being used)
def latest_sort(request):
  questions = Ask_it.objects.order_by('-created_at')

  context = { 'questions' : questions }
  return render(request, 'ask_it/home.html', context)

def ask_login(request):

  context = {  }
  return render(request, 'ask_it/login.html', context)

def ask_login_form(request):
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)
    return HttpResponseRedirect(reverse('ask_it:home'))
  else:
    return HttpResponseRedirect(reverse('ask_it:ask_login'))

def registration(request):


  context = { }
  return render(request, 'ask_it/registration.html',context)

def registration_form(request):
  next = request.GET.get('next', '/home')
  username = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']
  username_check = User.objects.filter(username=username).exists()
  if username_check==False and username.strip() and password.strip(): #checks for duplicate names/passwords, blank names/passwords, and names/passwords consisting only of white space
    user = User.objects.create_user(username, email, password)
    cookie_jar = Cookie_jar.objects.create(user=user)
    new_user=authenticate(request, username=username, password=password)
    login(request, new_user)

    return HttpResponseRedirect(reverse('ask_it:home'))
  else:
    # return HttpResponseRedirect(reverse('ask_it:registration',['sort=popular']))
    return HttpResponseRedirect(next)

  

@login_required
def question(request):

  context = { }
  return render(request, 'ask_it/question.html', context)

@login_required
def question_form(request):
  next = request.GET.get('next', '/home')
  question = request.POST['question']
  message = request.POST['message']
  upload = request.FILES.get('upload', None)
  caption = request.POST['caption']
  author = request.user
  if question.strip(): #checks for blank questions, and names/passwords consisting only of white space
    posting = Ask_it.objects.create(question=question.strip(), message=message, author=author, image=upload, image_caption=caption)
    upvote = Upvoted.objects.create(user=author, upvoted_questions=posting)

    return HttpResponseRedirect(reverse('ask_it:question_thread' , kwargs={'question_thread_id':posting.id}))
  else:
    return HttpResponseRedirect(next)

  

def question_thread(request, question_thread_id):
  question = Ask_it.objects.get(id=question_thread_id)

  context = { 'question' : question , 'question_thread_id' : question_thread_id}
  return render(request, 'ask_it/question_thread.html', context)

@login_required
def thread_reply(request,question_thread_id):
  next = request.GET.get('next', '/home')
  parent = Ask_it.objects.get(id=question_thread_id)
  message = request.POST['message']
  author = request.user
  if message and message.isspace() == False: #checks for blank and messages consisting only of whitespace
    reply = Reply.objects.create(message=message, author=author, parent=parent)
    upvote = Upvoted.objects.create(user=author, upvoted_reply=reply)
  
    return HttpResponseRedirect(reverse('ask_it:question_thread' , kwargs={'question_thread_id':question_thread_id}))
  else:
    return HttpResponseRedirect(next)


@login_required
def change_password(request):
  
  context = { }
  return render(request, 'ask_it/change_password.html', context)

# def add_username(request, context):
#   username = request.user

#   context['username'] = username 
#   return context

@login_required
def change_password_form(request):
  old_password = request.POST['old_password']
  new_password = request.POST['new_password']
  confirm_password = request.POST['confirm_password']
  check = request.user.check_password(old_password)
  if check == True and new_password == confirm_password and new_password.strip(): #checks old password, new and confirms password match, and new password is not blank or whitespace
    u = request.user
    u.set_password(new_password)
    u.save()
    logout(request)
    return HttpResponseRedirect(reverse('ask_it:ask_login'))
  else:
    return HttpResponseRedirect(reverse('ask_it:change_password'))

def ask_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('ask_it:home')) 