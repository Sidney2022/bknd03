from django.contrib import admin
from .models import Organisation, User as Profile
from django.contrib.auth.admin import UserAdmin


# class ProfileAdmin(UserAdmin):
#     model = Profile
#     list_display = ['email', 'userId','password',  'firstName', 'lastName']
#     list_filter = ['userId', 'email']
#     ordering = ['userId']
#     filter_horizontal = []
  
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'org_id', 'description']


admin.site.register(Profile)
admin.site.register(Organisation, OrganisationAdmin)