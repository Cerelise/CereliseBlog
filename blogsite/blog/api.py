from django.contrib.auth import models
from django.core import paginator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password, make_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.models import Article, Userinfo, Category, Comments, Favourite, Like
from django.contrib.auth.models import User, Group, Permission, ContentType
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import os
import base64
import requests
import datetime
import json

hostURL = 'http://127.0.0.1:9000/'


# 鉴权
@api_view(['POST'])
def wong_checkperm(request):
    token = request.POST['token']
    content_type = request.POST['contentType']
    permissions = json.loads(request.POST['permissions'])

    # print(token)
    # print(contentType)
    # print(permissions[0])
    user_token = Token.objects.filter(key=token)
    if user_token:
        user = user_token[0].user
        for p in permissions:
            app_str = content_type.split('_')[0]
            model_str = content_type.split('_')[1]
            perm_str = app_str + '.' + p + '_' + model_str
            # print(perm_str)
            check = user.has_perm(perm_str)
            # print(check)
            if check == False:
                return Response('noperm')
    else:
        return Response('nologin')

    return Response('ok')


# 登录
@api_view(['POST'])
def wong_login(request):
    username = request.POST['username']
    password = request.POST['password']
    # 登录逻辑
    user = User.objects.filter(username=username)
    if user:
        checkPwd = check_password(password, user[0].password)
        if checkPwd:
            userinfo = Userinfo.objects.get_or_create(belong=user[0])
            userinfo = Userinfo.objects.get(belong=user[0])
            token = Token.objects.get_or_create(user=user[0])
            token = Token.objects.get(user=user[0])
        else:
            return Response('pwd err')
    else:
        return Response('none')
    userinfo_data = {
        'token': token.key,
        'nickName': userinfo.nickName,
        'headImg': userinfo.headImg
    }
    return Response(userinfo_data)


# 注册
@api_view(['POST'])
def wong_register(request):
    username = request.POST['username']
    password = request.POST['password']
    repassword = request.POST['repassword']
    # 注册逻辑
    user = User.objects.filter(username=username)
    if user:
        return Response('repeat')
    else:
        new_password = make_password(password, username)
        newUser = User(username=username, password=new_password)
        newUser.save()

    token = Token.objects.get_or_create(user=newUser)
    token = Token.objects.get(user=newUser)
    userinfo = Userinfo.objects.get_or_create(belong=newUser)
    userinfo = Userinfo.objects.get(belong=newUser)
    userinfo_data = {
        'token': token.key,
        'nickName': userinfo.nickName,
        'headImg': userinfo.headImg
    }
    return Response(userinfo_data)


@api_view(['POST'])
def wong_reset_pwd(request):
    username = request.POST['username']
    password = request.POST['password']

    user = User.objects.filter(username=username)
    if not user:
        return Response('not_exist')
    else:
        new_password = make_password(password, username)
        User.objects.filter(username=username).update(password=new_password)
        new_user = User.objects.filter(username=username)
        print(new_user)
        return Response('ok')


#自动登录
@api_view(['POST'])
def wong_autoLogin(request):
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if user_token:
        userinfo = Userinfo.objects.get(belong=user_token[0].user)
        userinfo_data = {
            'token': token,
            'nickName': userinfo.nickName,
            'headImg': userinfo.headImg
        }
        return Response(userinfo_data)
    else:
        return Response('tokenTimeout')


#登出
@api_view(['POST'])
def wong_logout(request):
    token = request.POST['token']

    user_token = Token.objects.get(key=token)
    user_token.delete()
    return Response('logout')


# 查看文章
@api_view(['GET'])
def view_article(request):
    article_id = request.GET['article_id']
    article = Article.objects.get(id=article_id)
    article_data = {
        "title": article.title,
        "cover": article.cover,
        "describe": article.describe,
        "content": article.content,
        "nickName": article.belong.username,
        "category": "",
        "pre_id": 0,
        "next_id": 0,
    }

    pre_data = Article.objects.filter(id__lt=article_id)
    if pre_data:
        article_data["pre_id"] = pre_data.last().id
    next_data = Article.objects.filter(id__gt=article_id)
    if next_data:
        article_data["next_id"] = next_data.first().id

    if article.belong_category:
        article_data['category'] = article.belong_category.name

    return Response(article_data)


# 文章发布
@api_view(['POST', 'PUT'])
def add_article(request):
    if request.method == "PUT":
        token = request.POST['token']
        permList = ['blog.change_article']
        checkUser = userLoginAndPerm(token, permList)
        # print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)

        category_id = request.POST['category_id']
        article_id = request.POST['article_id']

        category = Category.objects.get(id=category_id)
        article = Article.objects.get(id=article_id)
        article.belong_category = category
        article.save()
        return Response("ok")

    title = request.POST['title']
    describe = request.POST['describe']
    cover = request.POST['cover']
    content = request.POST['content']
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('not login')
    if len(title) == 0:
        return Response('no title')

    # 保存文章
    new_article = Article(title=title)
    new_article.save()

    # 解析HTML文档
    soup = BeautifulSoup(content, 'html.parser')
    # 获取所有img标签的图片
    imgList = soup.find_all('img')
    # print(imgList)
    for img in range(0, len(imgList)):
        # print(imgList[img]['src'])
        src = imgList[img]['src']
        # 判断图片类型
        if 'http://' in src or 'https://' in src:
            # print('远程图片')
            # 请求远程图片
            image = requests.get(src)
            # 转换为二进制
            image_data = Image.open(BytesIO(image.content))
            # print(image_data)
            # 设定文件名
            # image_name = 时间 + 文件id +图片位标
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + \
                str(new_article.id) + '-' + str(img)
            image_data.save('upload/' + image_name + ".png")
            new_src = hostURL + 'upload/' + image_name + '.png'
            content = content.replace(src, new_src)
            # 封面设定
            if cover == src:
                cover = new_src
        else:
            # print('本地图片')
            image_data = base64.b64decode(src.split(',')[1])
            image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '-' + \
                str(new_article.id) + '-' + str(img) + '.' + \
                src.split(',')[0].split('/')[1].split(';')[0]
            # print(image_name)
            image_url = os.path.join('upload', image_name).replace('\\', '/')
            with open(image_url, 'wb') as f:
                f.write(image_data)
            # print(image_url)
            new_src = hostURL + image_url
            content = content.replace(src, new_src)
            # 封面设定
            if cover == src:
                cover = new_src

    new_article.content = content
    new_article.describe = describe
    new_article.cover = cover
    new_article.belong = user_token[0].user
    new_article.save()
    return Response('ok')


# 文章分页 数据列表
@api_view(['GET'])
def article_list(request):
    # if request.method == 'GET':
    #     pass
    page = request.GET['page']
    pageSize = request.GET['pageSize']
    category = request.GET['category']
    if category == 'all':
        articles = Article.objects.all()
    elif category == 'nobelong':
        articles = Article.objects.filter(belong_category=None)
    else:
        articles = Article.objects.filter(belong_category__name=category)
    total = len(articles)
    paginator = Paginator(articles, pageSize)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    # print(articles)
    articles_data = []
    for a in articles:
        a_item = {
            'title': a.title,
            'cover': a.cover,
            'nickName': '',
            'id': a.id,
        }
        article_user = a.belong
        userinfo = Userinfo.objects.filter(belong=article_user)
        if userinfo[0].nickName:
            a_item['nickName'] = userinfo[0].nickName
        else:
            a_item['nickName'] = article_user.username
        articles_data.append(a_item)
    return Response({'data': articles_data, 'total': total})


# 删除文章
@api_view(['DELETE'])
def delete_article(request):
    article_id = request.POST['id']
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')

    user = user_token[0].user
    user_perm = user.has_perm('blog.delete_article')
    print('文章删除权限')
    if user_perm == False:
        return Response('noperm')
    print(article_id)

    article = Article.objects.get(id=article_id)
    article.delete()
    return Response('ok')


# 用户列表获取
@api_view(['GET'])
def wong_userlist(request):
    user_list = User.objects.all()
    user_list_data = []
    for user in user_list:
        user_item = {"name": user.username}
        user_list_data.append(user_item)
    return Response(user_list_data)


# 用户组管理
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def wong_group(request):
    # 获取用户组列表
    if request.method == "GET":
        groups = Group.objects.all()
        group_data = []
        for g in groups:
            g_item = {"name": g.name}
            group_data.append(g_item)
        return Response(group_data)

    # 分配用户 用户组
    if request.method == "POST":
        token = request.POST['token']
        permList = [
            'auth.add_user', 'suth.delete_user', 'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        # print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)

        group_name = request.POST['group']
        userlist_name = json.loads(request.POST['userlist'])

        group = Group.objects.get(name=group_name)

        for username in userlist_name:
            user = User.objects.get(username=username)
            # user.groups.add(group)
            group.user_set.add(user)
        return Response('ok')

    # 新建用户组
    if request.method == "PUT":
        token = request.POST['token']
        permList = [
            'auth.add_user', 'suth.delete_user', 'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        # print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        new_name = request.POST['new_group']
        perm_list = json.loads(request.POST['perm_list'])

        new_group = Group.objects.filter(name=new_name)
        if new_group:
            return Response("same name")
        new_group = Group.objects.create(name=new_name)
        for perm in perm_list:
            app_str = perm['content_type'].split('_')[0]
            model_str = perm['content_type'].split('_')[1]
            contentType = ContentType.objects.get(app_label=app_str,
                                                  model=model_str)
            for method in perm['perm_methods']:
                print(method)
                codename = method + '_' + model_str
                permission = Permission.objects.get(content_type=contentType,
                                                    codename=codename)
                new_group.permissions.add(permission)
        return Response('ok')

    # 删除用户组列表
    if request.method == 'DELETE':
        token = request.POST['token']
        permList = [
            'auth.add_user', 'suth.delete_user', 'auth.change_user',
            'auth.view_user'
        ]
        checkUser = userLoginAndPerm(token, permList)
        # print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        name = request.POST['name']
        group = Group.objects.get(name=name)
        group.delete()
        return Response("ok")


# 检查用户登录与权限
def userLoginAndPerm(token, permlist):
    user_token = Token.objects.filter(key=token)
    if user_token:
        user = user_token[0].user
        for perm_str in permlist:
            perm_user = user.has_perm(perm_str)
            if perm_str:
                return 'perm_pass'
            else:
                # 403
                return 'noperm'
    else:
        return 'nologin'


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
def wong_category(request):
    if request.method == "GET":
        category = Category.objects.filter(belong=None)

        category_data = loopGetCategory(category)
        return Response(category_data)

    if request.method == "DELETE":
        token = request.POST['token']
        permList = ['blog.delete_category']
        checkUser = userLoginAndPerm(token, permList)
        # print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)

        category_id = request.POST['id']
        category = Category.objects.get(id=category_id)
        category.delete()
        return Response('ok')

    if request.method == "PUT":
        token = request.POST['token']
        permList = [
            'blog.add_category', 'blog.delete_category', 'blog.change_category',
            'blog.view_category'
        ]
        checkUser = userLoginAndPerm(token, permList)
        # print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)

        category_tree = json.loads(request.POST['category_tree'])
        print(category_tree)
        loopSaveCategory(category_tree, None)
    return Response('ok')


# 循环获取栏目数据
def loopGetCategory(category_list):
    category_data = []
    for category in category_list:
        category_item = {
            "id": category.id,
            "label": category.name,
            "children": [],
            "article_num": len(category.article_category.all())
        }
        children = category.category_children.all()
        if children:
            children_data = loopGetCategory(children)
            for c in children_data:
                category_item['children'].append(c)
        category_data.append(category_item)
    return category_data


# 循环保存栏目树形结构
def loopSaveCategory(tree_data, parent_id):
    parent_category = Category.objects.filter(id=parent_id)
    if parent_category:
        for tree in tree_data:
            saved_category = Category.objects.filter(id=tree['id'])
            if saved_category:
                saved_category[0].belong = parent_category[0]
                saved_category[0].save()
                if len(tree['children']) > 0:
                    loopSaveCategory(tree['children'], saved_category[0].id)
            else:
                new_category = Category(name=tree['label'],
                                        belong=parent_category[0])
                new_category.save()
                if len(tree['children']) > 0:
                    loopSaveCategory(tree['children'], new_category.id)

    else:
        for tree in tree_data:
            saved_category = Category.objects.filter(id=tree['id'])
            if saved_category:
                saved_category[0].belong = None
                saved_category[0].save()
                loopSaveCategory(tree['children'], saved_category[0].id)
            else:
                new_category = Category(name=tree['label'])
                new_category.save()
                if len(tree['children']) > 0:
                    loopSaveCategory(tree['children'], new_category.id)
    return


@api_view(['GET', 'POST'])
def wong_comment(request):
    if request.method == "GET":
        article_id = request.GET['article_id']
        pagesize = request.GET['pageSize']
        page = request.GET['page']
        article = Article.objects.get(id=article_id)

        comments = Comments.objects.filter(belong=article)[::-1]

        total = len(comments)
        paginator = Paginator(comments, pagesize)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        comment_data = []
        for comment in comments:
            comment_item = {
                "nickName": comment.belong_user.username,
                "text": comment.text
            }
            comment_data.append(comment_item)
        return Response({"data": comment_data, "total": total})

    if request.method == "POST":
        token = request.POST['token']
        permList = ['blog.view_article']
        checkUser = userLoginAndPerm(token, permList)
        print(checkUser)
        if checkUser != 'perm_pass':
            return Response(checkUser)
        article_id = request.POST['article_id']
        text = request.POST['text']

        article = Article.objects.get(id=article_id)
        user = Token.objects.get(key=token).user

        new_comment = Comments(belong_user=user, belong=article, text=text)
        new_comment.save()
        return Response('ok')


@api_view(['POST'])
def userArticleInfo(request):
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')
    article_id = request.POST['article_id']
    article = Article.objects.get(id=article_id)
    user = user_token[0].user

    user_article_info = {"like": False, "favor": False}

    liked = Like.objects.filter(belong=article, belong_user=user)
    if liked:
        user_article_info['like'] = True

    favored = Favourite.objects.filter(belong=article, belong_user=user)
    if favored:
        user_article_info['favor'] = True
    return Response(user_article_info)


@api_view(['POST'])
def article_like(request):
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')

    article_id = request.POST['article_id']
    article = Article.objects.get(id=article_id)

    liked = Like.objects.filter(belong=article, belong_user=user_token[0].user)

    if liked:
        liked[0].delete()
        return Response('ok')
    else:
        new_like = Like(belong=article, belong_user=user_token[0].user)
        new_like.save()
        return Response('ok')


@api_view(['POST'])
def article_favor(request):
    token = request.POST['token']

    user_token = Token.objects.filter(key=token)
    if len(user_token) == 0:
        return Response('nologin')

    article_id = request.POST['article_id']
    article = Article.objects.get(id=article_id)

    favored = Favourite.objects.filter(belong=article,
                                       belong_user=user_token[0].user)

    if favored:
        favored[0].delete()
        return Response('ok')
    else:
        new_favor = Favourite(belong=article, belong_user=user_token[0].user)
        new_favor.save()
        return Response('ok')
