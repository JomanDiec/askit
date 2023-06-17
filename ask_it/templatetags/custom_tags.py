from django import template
from django.utils import timezone
from ask_it.models import *

register = template.Library()

@register.simple_tag(takes_context=True)
def upvote_filter(context, user, question): #checks if user has upvoted post or not, changes color of chevron and upvote number if true
  user = context['request'].user
  if user.is_authenticated:
    if Upvoted.objects.filter(user=user, upvoted_questions=question).exists():
      return 'color:#FF5733'
    else:
      return ''
  else:
    return '' #for guests/logged out users

@register.simple_tag(takes_context=True)
def reply_filter(context, user, reply):
  user = context['request'].user
  if user.is_authenticated:
    if Upvoted.objects.filter(user=user, upvoted_reply=reply).exists():
      return 'color:#FF5733'
    else:
      return ''
  else:
    return ''

def modify_name(value, arg):

    # if arg is first_name: return the first string before space

    if arg == "first_name":

        return value.split(" ")[0]

    # if arg is last_name: return the last string before space

    if arg == "last_name":

        return value.split(" ")[-1]

    # if arg is title_case: return the title case of the string

    if arg == "title_case":

        return value.title()

    return value

    

register.filter('modify_name', modify_name)

import datetime


@register.simple_tag

def current_time(format_string):

  return datetime.datetime.now().strftime(format_string)

@register.simple_tag

def mute(*args):

    return ""

# An upper function that capitalizes word passed to it.
@register.simple_tag

def upper(args):
  return args.upper()

# An upper function that capitalizes the first letter of the word passed to it.
# @register.filter(name='modify_name')
# def modify_name(value):
#     return value.title()

# An upper function that sets returns a red color.
@register.filter(name='get_color')
def color(value):
    if value:
        return "#FF0000"