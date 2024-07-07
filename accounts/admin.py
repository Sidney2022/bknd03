from django.contrib import admin
from .models import Organisation, User as Profile
from django.contrib.auth.admin import UserAdmin


# class ProfileAdmin(UserAdmin):
#     model = Profile
#     list_display = [ 'user_id', 'email', 'first_name', 'last_name']
  
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['name', 'org_id', 'description']

admin.site.register(Profile)
admin.site.register(Organisation, OrganisationAdmin)