from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from blog.models import Article, Userinfo, Category, Comments, Favourite, Like

# Register your models here.

admin.site.register(Article)
admin.site.register(Userinfo)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(Favourite)
admin.site.register(Like)
# admin.site.register(UserAdmin)