from django.urls import path
from rest_framework.decorators import api_view
from blog import api

urlpatterns = [
    # 文章管理

    # 文章发布
    path('add-article/', api.add_article),
    # 文章列表
    path('article-list/', api.article_list),
    # 文章删除
    path('delete-article/', api.delete_article),
    # 文章查看
    path('view-article/', api.view_article),

    # 用户管理

    # 登录
    path('wong-login/', api.wong_login),
    # 注册
    path('wong-register/', api.wong_register),
    # 修改密码
    path('wong-resetpwd/', api.wong_reset_pwd),
    # 自动登录
    path('wong-autologin/', api.wong_autoLogin),
    # 登出
    path('wong-logout/', api.wong_logout),
    # 鉴权
    path('wong-checkperm/', api.wong_checkperm),
    # 用户列表
    path('wong-userlist/', api.wong_userlist),
    # 用户组
    path('wong-group/', api.wong_group),

    # 栏目管理
    path('wong-category/', api.wong_category),

    # 用户互动
    path('wong-comment/', api.wong_comment),
    path('user-article-info/', api.userArticleInfo),
    path('article-like/', api.article_like),
    path('article-favor/', api.article_favor)
]
