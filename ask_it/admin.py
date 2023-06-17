from django.contrib import admin

from .models import *

admin.site.register(Ask_it)
admin.site.register(Cookie_jar)
admin.site.register(QuestionImage)

# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.models import User

# # Define an inline admin descriptor for Employee model
# # which acts a bit like a singleton
# class Ask_itInline(admin.StackedInline):
#     model = Ask_it
#     can_delete = False
#     verbose_name_plural = 'Ask_it'

# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (Ask_itInline,)

# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)