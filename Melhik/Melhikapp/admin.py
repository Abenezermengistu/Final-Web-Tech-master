from django.contrib import admin
from . import models
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(models.Message)
admin.site.register(models.ChatRoom)
admin.site.register(models.CustomUser, UserAdmin)
admin.site.register(models.Freelancer)
admin.site.register(models.Job)
admin.site.register(models.ProjectProposal)
admin.site.register(models.Review)