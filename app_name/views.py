from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.contrib.sessions.backends.db import SessionStore
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Sum
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import shutil
import openai
from django.conf import settings
import uuid
from .models import User, Case
from .form import AvatarForm,OfferForm
from .serializers import UserSerializer, CaseSerializer
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils import timezone
from .models import Article, Like, Comment
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from django.db.models import Count, Q
from django.http import JsonResponse
from collections import defaultdict
from .models import User, Article, Like, Comment,PrivateMessage,Feedback,TeamIntroduction,TeamMember,worker,FeaturedArticle,Alumni,Offer,Tag,UserLoginRecord,School,Major
import re
from django.db import models
import json
import requests
import http.client
import json
from django.http import JsonResponse
import openai
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import Http404

def dashboard(request):
    user_count = User.objects.count()
    article_count = Article.objects.count()
    offer_count = Offer.objects.count()
    feedback_count = Feedback.objects.count()
    Alumni_count = Alumni.objects.count()
    today = timezone.now().date()
    login_records = UserLoginRecord.objects.filter(login_time__date=today)
    num_logins_today = len(set(login_records.values_list('user_id', flat=True)))
    print("今日登录用户数为：",num_logins_today)
    Comment_count = Comment.objects.count()
    Like_count = Like.objects.count()
    # 计算不同分段学生的百分比
    gpa_ranges = [
        (0, 2),
        (2, 2.5),
        (2.5, 3),
        (3, 3.5),
        (3.5, 3.8),
        (3.8, float('inf')),
    ]
    gpa_percentages = []
    institution_offers = Offer.objects.all()
    institution_offers_count = institution_offers.count()
    for gpa_min, gpa_max in gpa_ranges:
        gpa_range_count = institution_offers.filter(gpa__gte=gpa_min, gpa__lt=gpa_max).count()
        gpa_range_percentage = round(gpa_range_count / institution_offers_count * 100, 2)
        gpa_percentages.append(gpa_range_percentage)
    
    article_publish_past_week = []
    for i in range(7):
        past_day = today - timedelta(days=i)
        article_publish_past_day = Article.objects.filter(created_at__date=past_day)
        num_article_publish_past_day = len(set(article_publish_past_day.values_list()))
        article_publish_past_week.append(num_article_publish_past_day)
    print(article_publish_past_week)
    context = { 'user_count': user_count, 
               'article_count': article_count,
               "offer_count":offer_count,
               "feedback_count":feedback_count,
               "Alumni_count":Alumni_count,
               "num_logins_today":num_logins_today,
               "Comment_count":Comment_count,
               "Like_count":Like_count,
               "gpa_percentages": gpa_percentages,
               "article_publish_past_week":json.dumps(article_publish_past_week)}
    return render(request, 'src/dashboard.html',context)



def manage_account(request):
    schools = School.objects.all()
    majors = Major.objects.all()
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        
    except:
        pass

    # 获取用户点赞过的、评论过的、以及写过的所有文章对象
    liked_articles = set(user.liked_articles.all()) if user else set()
    commented_articles = set([comment.article for comment in user.comment_set.all()]) if user else set()
    authored_articles = set(user.authored_articles.all()) if user else set()
    articles = list(liked_articles.union(commented_articles, authored_articles))
    # 获取这些文章的所有tag，并且去重
    tags = set()
    for article in articles:
        for tag in article.tags.all():
            tags.add(tag)
            
    articles_written_byuser = Article.objects.filter(author=user)[:10]
    private_message = get_latest_messages(user)
    return render(request, 'src/manage_account.html',{
        "user":user,
        "personal_article":articles_written_byuser,
        "private_message":private_message,
        "tags":tags,
        "schools":schools,
        "majors":majors
    })

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	


def create_feedback(request):
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",request.method)
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data.get('content', '')
        print("发送来的信息是：", content)
        username = request.session.get('username')
        print("是我发送的：",username)
        user = User.objects.get(username=username)

        if content:
            print("确实是跑进来了啊！！！")
            feedback = Feedback.objects.create(sender=user, content=content,sent_at=timezone.now())
            print("反馈也成功创建了啊！",feedback)
            
            return JsonResponse({'success': True, 'message': '感谢您的反馈。我们的团队已经收到了，并会在几个小时内回复您。'})
        else:
            return JsonResponse({'success': False, 'message': '请提供反馈内容。'})
    else:
        return JsonResponse({'success': False, 'message': '无效的请求方法。'})



def user_activity_data(request, username):
    # Get the user
    user = User.objects.get(username=username)

    # Calculate the start date (15 days ago from now)
    start_date = datetime.now() - timedelta(days=15)

    # Filter articles, likes, and comments created by the user in the given time range
    articles = Article.objects.filter(author=user, created_at__gte=start_date).annotate(date=models.functions.TruncDate('created_at')).values('date').annotate(count=models.Count('id')).values('date', 'count')
    likes = Like.objects.filter(user=user, liked_at__gte=start_date).annotate(date=models.functions.TruncDate('liked_at')).values('date').annotate(count=models.Count('id')).values('date', 'count')
    comments = Comment.objects.filter(user=user, created_at__gte=start_date).annotate(date=models.functions.TruncDate('created_at')).values('date').annotate(count=models.Count('id')).values('date', 'count')

    # Combine the data
    activity_data = defaultdict(lambda: {"articles_count": 0, "likes_count": 0, "comments_count": 0})

    for article in articles:
        activity_data[article['date']]['articles_count'] = article['count']

    for like in likes:
        activity_data[like['date']]['likes_count'] = like['count']

    for comment in comments:
        activity_data[comment['date']]['comments_count'] = comment['count']

    # Remove dates with all activity counts equal to 0 and sort by date
    activity_data = {k: v for k, v in activity_data.items() if sum(v.values()) > 0}
    activity_data = sorted(activity_data.items(), key=lambda x: x[0], reverse=True)[:15]

    # Return the activity data as a JsonResponse
    return JsonResponse({"activity_data": activity_data})


def qurrey_user(account,password):
    try:
        status = User.objects.filter(account_number = account, password = password)[0]
    except:
        status = None
    return status

def index(request):
    return render(request, 'index.html')

def tag_articles(request, tag_name):
    print("跑进这个函数了")
    print("用户要找的tag为：",tag_name)
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        articles_written_byuser = Article.objects.filter(author=user)[:10]
        print("用户创建成功了")
    except:
        user = None
        
    try:
        tag = Tag.objects.get(name=tag_name)
    except Tag.DoesNotExist:
        raise Http404("Tag does not exist")
    articles = tag.articles.all()
    
    return render(request, 'src/tag_result.html', {'tag': tag, 'articles': articles,"user":user,"personal_article":articles_written_byuser})


def write_blog(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    articles_written_byuser = Article.objects.filter(author=user)[:10]
    return render(request, 'src//Write.html',{"user":user,"personal_article":articles_written_byuser})


def search_offers(request):
    print("至少跑进来了！")
    if request.method == 'GET':
        search_type = request.GET.get('search', '')
        search_query = request.GET.get('q', '')
        offers = Offer.objects.filter(is_valid=True)
        print("")
        if search_query:
            if search_type == 'ielts_score':
                try:
                    ielts_score = float(search_query)
                    min_ielts_score = ielts_score - 0.5
                    max_ielts_score = ielts_score + 0.5
                    offers = offers.filter(
                        Q(ielts_score__gte=min_ielts_score) & Q(ielts_score__lte=max_ielts_score))
                except ValueError:
                    pass
            elif search_type == 'gpa':
                try:
                    gpa = float(search_query)
                    min_gpa = gpa - 0.1
                    max_gpa = gpa + 0.1
                    offers = offers.filter(
                        Q(gpa__gte=min_gpa) & Q(gpa__lte=max_gpa))
                except ValueError:
                    pass
            elif search_type == 'institution':
                offers = offers.filter(institution__icontains=search_query)
            elif search_type == 'major':
                offers = offers.filter(major__icontains=search_query)

        offers = offers.order_by('-offer_id')
        username = request.session.get('username')

        try:
            user = User.objects.get(username=username)
        except:
            user = None
        articles_written_byuser = Article.objects.filter(author=user)[:10]
        
        return render(request, 'src/search_result.html', {"user":user,'offers': offers,"personal_article":articles_written_byuser})



def search(request):
    print("其实是跑到这里来咯！")
    username = request.session.get('username')

    try:
        user = User.objects.get(username=username)
    except:
        user = None
    articles_written_byuser = Article.objects.filter(author=user)[:10]
    offers = Offer.objects.filter(is_valid=True)
    return render(request, 'src/search.html',{"user":user,"offers":offers,"personal_article":articles_written_byuser})


def Personal_homepage(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        
    except:
        print("问题出现在这里啊！")
        pass
    
    # 获取用户点赞过的、评论过的、以及写过的所有文章对象
    liked_articles = set(user.liked_articles.all()) if user else set()
    commented_articles = set([comment.article for comment in user.comment_set.all()]) if user else set()
    authored_articles = set(user.authored_articles.all()) if user else set()
    articles = list(liked_articles.union(commented_articles, authored_articles))
    
    # 获取这些文章的所有tag，并且去重
    tags = set()
    for article in articles:
        for tag in article.tags.all():
            tags.add(tag)
            
    articles_written_byuser = Article.objects.filter(author=user)[:10]
    private_message = get_latest_messages(user)
    return render(request, 'src/archive.html',{
        "user":user,
        "articles": articles,
        "personal_article":articles_written_byuser,
        "private_message":private_message,
        "tags":tags
    })



def Personal_homepage_other(request,username):
    username_self = request.session.get('username')
    print("##############################")
    print("本人：",username_self)
    try:
        user = User.objects.get(username=username_self)
        user_other = User.objects.get(username=username)
        print("##############################")
        print("本人：",user)
        print("发现了：",user_other)
    except:
        pass
    # 获取用户点赞过的、评论过的、以及写过的所有文章对象
    liked_articles = set(user_other.liked_articles.all()) if user_other else set()
    commented_articles = set([comment.article for comment in user_other.comment_set.all()]) if user_other else set()
    authored_articles = set(user.authored_articles.all()) if user_other else set()
    articles = list(liked_articles.union(commented_articles, authored_articles))
    articles_written_byuser = Article.objects.filter(author=user_other)[:10]

    
    # 获取这些文章的所有tag，并且去重
    tags = set()
    for article in articles:
        for tag in article.tags.all():
            tags.add(tag)

    return render(request, 'src/archive_user.html',{"user":user,"user_other":user_other,"articles": articles,"personal_article":articles_written_byuser,"tags":tags})


def send_message(request, recipient_username):
    recipient = User.objects.get(username=recipient_username)
    username_1 = request.session.get('username')
    try:
        sender = User.objects.get(username=username_1)
    except:
        return redirect(current_url)
    if request.method == 'POST':
        content = request.POST['content']
        if content:
            message = PrivateMessage.objects.create(
                sender  = sender,
                recipient=recipient,
                content=content,
                sent_at=timezone.now()
            )
            messages.success(request, 'Your message was sent successfully.')

            # 获取当前页面的 URL，并使用它进行重定向
            current_url = request.POST.get('current_url', 'index')
            return redirect(current_url)
        else:
            messages.error(request, 'Your message was empty. Please try again.')



    context = {'recipient': recipient}
    return redirect(request.path)

def get_latest_messages(user):
    latest_messages = PrivateMessage.objects.filter(recipient=user).order_by('-sent_at')[:20]
    return latest_messages


from django.core.paginator import Paginator

from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Count

def followed_blog_list_follow(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        followed_authors = user.idols.all() # 获取当前用户关注的博主列表
        print("+++++++++++++++++++++++++++++\n全场的目光看向我，我是阳光开朗大男孩：",followed_authors)
        articles = Article.objects.filter(author__in=followed_authors).annotate(likes_count=Count('likes')).order_by('-id')
        articles_written_byuser = Article.objects.filter(author=user).order_by('-id')[:10]
    except:
        user = None
        articles = None
        articles_written_byuser = None

    private_message = get_latest_messages(user)

    # 获取当前页数
    page_number = request.GET.get('page')

    # 实例化分页对象，并指定每页显示10篇文章
    paginator = Paginator(articles, 16)

    # 获取当前页的文章列表
    page_obj = paginator.get_page(page_number)

    return render(request, 'src/elements_follow.html', {"user": user, "articles": page_obj, "personal_article": articles_written_byuser, "private_message": private_message})


def blog_list(request):
    articles = Article.objects.annotate(likes_count=Count('likes')).order_by('-id')
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        articles_written_byuser = Article.objects.filter(author=user).order_by('-id')[:10]
    except:
        user = None
        articles_written_byuser = None
    
    private_message = get_latest_messages(user)
    
    # 获取当前页数
    page_number = request.GET.get('page')
    
    # 实例化分页对象，并指定每页显示10篇文章
    paginator = Paginator(articles, 16)
    
    # 获取当前页的文章列表
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'src/elements.html', {"user": user, "articles": page_obj, "personal_article": articles_written_byuser, "private_message": private_message})



def upload_avatar(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded avatar to a temporary path
            temp_path = 'temp_avatar.jpg'
            with open(temp_path, 'wb') as f:
                f.write(request.FILES['avatar'].read())
            # Move the uploaded avatar to the static/avatars directory
            avatar_path = os.path.join(settings.BASE_DIR, 'app_name', 'static', 'avatars', f'{user.username}.jpg')
            shutil.move(temp_path, avatar_path)
            # Update the user's avatar field in the database
            user.avatar = os.path.join('avatars', f'{user.username}.jpg')
            user.save()
            return redirect('management')
    else:
        form = AvatarForm()
    print("################################\n代码出现了报错\n################################")
    return redirect('management')


def modify_password_here(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        user = request.session.get('user') # 从session中获取用户信息
        if old_password == user['password']:
            if new_password == confirm_password:
                user['password'] = new_password # 更新密码 
                messages.success(request, 'Your password was successfully updated!')
                return redirect('management')
            else:
                messages.error(request, 'New passwords do not match. Please try again.')
        else:
            messages.error(request, 'Incorrect old password. Please try again.')
    return redirect('management')




def update_personal_statement(request):
    # 获取当前登录用户
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        user = None

    if request.method == 'POST':
        user.personal_statement = request.POST['personal_statement']
        user.save()
        return redirect('management')

    return redirect('management')



def signup(request):

    return render(request, 'signup.html')




from django.db.models import Count, F
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import timedelta
from django.utils import timezone

def bloger(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('index')
    try:
        team_intro = TeamIntroduction.objects.get()
    except TeamIntroduction.DoesNotExist:
        team_intro = None
    team_members = TeamMember.objects.all()
    admins = worker.objects.all()
    latest_articles = Article.objects.order_by('-id')[:10]
    Article_selected = FeaturedArticle.objects.all()

    # Get the date one month ago
    one_month_ago = timezone.now() - timedelta(days=30)

    # Calculate the total number of articles, comments, and likes for each user within the past month
    active_users = User.objects.filter(
        authored_articles__created_at__gte=one_month_ago
    ).annotate(
        total_activity=Count('authored_articles') + Count('liked_articles') + Count('comment')
    ).order_by('-total_activity')[:10]

    return render(request, 'src//index.html',{"user":user,"team_intro": team_intro,"team_members": team_members,"admins":admins,"latest_articles":latest_articles,"Article_selected":Article_selected, "active_users": active_users})


def login_view(request):
    if request.method == "POST":
        account  = request.POST["account_number"]
        password = request.POST["password"]
        user_status = qurrey_user(account,password)
        if user_status is not None:
            user = User.objects.get(account_number=account,password=password)
            request.session["username"] = user.username
            request.session["email"] = user.email
            request.session["account_number"] = user.account_number
            login_record = UserLoginRecord(user=user, login_time=timezone.now(), login_ip=request.META.get('REMOTE_ADDR'))
            login_record.save()
            return redirect('blog')
        else:
            return render(request, 'index.html',{'error':'Invalid account or password. Tru again please.'})
    else:
        return render(request, 'index.html')

def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        account_number = request.POST["account_number"]

        # 检查用户名和账号是否已经存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在，请选择其他用户名。')
            return render(request, 'register.html')

        if User.objects.filter(account_number=account_number).exists():
            messages.error(request, '账号已存在，请使用其他账号。')
            return render(request, 'register.html')

        # 创建新用户并保存到数据库
        user = User(username=username, email=email, password=password, account_number=account_number)
        user.save()

        # 注册成功后，将新用户信息存入 session
        request.session["username"] = user.username
        request.session["email"] = user.email
        request.session["account_number"] = user.account_number

        # 重定向到 blog 页面
        return redirect('blog')

    else:
        return render(request, 'signup.html')



@require_POST
def create_offer(request):
    username_1 = request.session.get('username')
    try:
        user = User.objects.get(username=username_1)
    except:
        user = None
    form = OfferForm(request.POST, request.FILES)
    max_id = Offer.objects.aggregate(models.Max('offer_id'))['offer_id__max'] or 0

    if form.is_valid():
        offer = form.save(commit=False)
        offer.applicant = user

        
        # Save the uploaded avatar to a temporary path
        temp_path = 'temp_avatar.jpg'
        with open(temp_path, 'wb') as f:
            f.write(request.FILES['offer_image'].read())
         # Move the uploaded avatar to the static/avatars directory
        print("全场目光看过来！这里有新鲜出炉的id：",offer.offer_id)
        avatar_path = os.path.join(settings.BASE_DIR, 'app_name', 'static', 'offers', f'{str(max_id+1)}.jpg')
        shutil.move(temp_path, avatar_path)
        offer.offer_image = os.path.join('offers', f'{str(max_id+1)}.jpg')
        offer.save()
    return redirect('management')




def register_view_alumi(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        account_number = request.POST["account_number"]
        gpa = request.POST["gpa"]
        graduation_destination = request.POST["graduation_destination"]

        # 检查用户名和账号是否已经存在
        if User.objects.filter(username=username).exists():
            messages.error(request, '用户名已存在，请选择其他用户名。')
            return render(request, 'register.html')

        if User.objects.filter(account_number=account_number).exists():
            messages.error(request, '账号已存在，请使用其他账号。')
            return render(request, 'register.html')

        # 创建新用户并保存到数据库
        user = Alumni(username=username, email=email, password=password, account_number=account_number,gpa=gpa,graduation_destination=graduation_destination)
        user.save()

        # 注册成功后，将新用户信息存入 session
        request.session["username"] = user.username
        request.session["email"] = user.email
        request.session["account_number"] = user.account_number

        # 重定向到 blog 页面
        return redirect('blog')

    else:
        return render(request, 'signup_alumni.html')
    
def signup_alumni(request):
    return render(request, 'signup_alumni.html')

def test_avdar(request):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        pass
    print("################################################")
    print("图像在这里：",user.avatar.url)
    print("################################################")

def write_article(request):
    print("测试升级后的功能是否正常！")
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        username = request.session.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            return redirect('write')

        is_alumni = False
        try:
            alumni = Alumni.objects.get(username=username)
            if alumni:
                is_alumni = True
        except Alumni.DoesNotExist:
            pass

        article = Article(author=user, title=title, content=content, is_alumni=is_alumni)
        article.save()

        # 处理标签
        # 处理标签
        tag_input = request.POST.get("tags", "").strip()  # 获取标签输入，去掉首尾空格
        if tag_input:
            tag_names = [name.strip() for name in re.split(r'#\s*', tag_input) if name.strip()]  # 使用正则表达式查找标签名称，并按 # 分割成多个名称
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)  # 获取或创建标签
                article.tags.add(tag)  # 将标签添加到文章中

        return redirect('blog_list')
    return redirect('blog_list')





def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    print("################################找到文章了")
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        articles_written_byuser = Article.objects.filter(author=article.author)[:10]
    except:
        return redirect('blog')
    tags = article.tags.all()
    is_liked = user is not None  and user in article.likes.all()
    private_message = get_latest_messages(user)
    return render(request, 'src//article.html', {'article': article,'is_liked':is_liked,"user":user,"personal_article":articles_written_byuser,"private_message":private_message,"tags":tags})



from django.db.models import When, F, Q



def search_articles(request):
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(Q(title__icontains=query) | Q(tags__name__icontains=query) | Q(author__username__icontains=query) | Q(content__icontains=query)).order_by('-created_at')
    else:
        articles = []
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        articles_written_byuser = Article.objects.filter(author=user)
    except:
        user = None
    context = {
        'articles': articles,
        'query': query,
        "user":user,
        "personal_article":articles_written_byuser
    }
    return render(request, 'src/blog_result.html', context=context)




def offer_detail(request, pk):
    schools = School.objects.all()
    # 获取该offer的信息
    offer = Offer.objects.get(offer_id=pk)

    # 计算比该offer雅思成绩高的offer数量以及总offer数量
    higher_ielts_count = Offer.objects.filter(ielts_score__gt=offer.ielts_score).count()
    total_offers_count = Offer.objects.count()
    # 计算比该offer GPA高的offer数量
    higher_gpa_count = Offer.objects.filter(gpa__gt=offer.gpa).count()

    # 计算比该offer高的百分比
    higher_ielts_percent = round(higher_ielts_count / total_offers_count * 100, 2)
    higher_gpa_percent = round(higher_gpa_count / total_offers_count * 100, 2)

    # 计算不同分段学生的百分比
    gpa_ranges = [
        (0, 2),
        (2, 2.5),
        (2.5, 3),
        (3, 3.5),
        (3.5, 3.8),
        (3.8, float('inf')),
    ]
    gpa_percentages = []
    institution_offers = Offer.objects.filter(institution=offer.institution)
    institution_offers_count = institution_offers.count()
    for gpa_min, gpa_max in gpa_ranges:
        gpa_range_count = institution_offers.filter(gpa__gte=gpa_min, gpa__lt=gpa_max).count()
        gpa_range_percentage = round(gpa_range_count / institution_offers_count * 100, 2)
        gpa_percentages.append(gpa_range_percentage)

    # 获取用户信息和该用户最近写的10篇文章
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
        articles_written_byuser = Article.objects.filter(author=offer.applicant)[:10]
    except:
        return redirect('blog')

    # 将计算出的比例和用户信息传递给模板
    return render(request, 'src//offer.html', {'Offer': offer, "user":user,
                                               "personal_article":articles_written_byuser,
                                               "higher_ielts_percent": higher_ielts_percent,
                                               "higher_gpa_percent": higher_gpa_percent,
                                               "gpa_percentages": gpa_percentages,
                                               "schools":schools})


def write_comment(request,article_id):
    article = get_object_or_404(Article, id=article_id)
    content = request.POST["content"]
    username = request.session.get('username')
    if request.method == "POST":
        try:
            user = User.objects.get(username=username)
        except:
            return redirect('blog')
        new_comment = Comment(user=user,article = article, content = content)
        new_comment.save()
        return redirect('article_detail', pk=article.id)
    else:
        return redirect('article_detail', pk=article.id)

def follow(request,username_idol):
    username = request.session.get('username')
    try:
        user = User.objects.get(username=username)
    except:
        return redirect('blog')
    user_to_follow = get_object_or_404(User, username=username_idol)
    # 添加当前登录用户到要关注的用户的粉丝列表中
    user_to_follow.fans.add(user)
    messages.success(request, f"You are now following {user_to_follow.username}")
    return redirect('personal_homepage_other', username=user_to_follow.username)

def like_article_new(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        username = request.session.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            return redirect('article_detail', pk=article.id)
        print(user)
        if user is not None and user not in article.likes.all():
            Like.objects.create(user=user, article=article)
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def cancel_like(request,article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, id=article_id)
        username = request.session.get('username')
        try:
            user = User.objects.get(username=username)
        except:
            return redirect('article_detail', pk=article.id)
        try:
            like = Like.objects.get(user=user,article=article)
            like.delete()
            return JsonResponse({'success': True})
        except:
            pass
    return JsonResponse({'success': False})


#--------------------------------------------API---------------------------------------------------------------#
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(UserList, self).dispatch(*args, **kwargs)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(UserDetail, self).dispatch(*args, **kwargs)

class CaseList(generics.ListCreateAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(CaseList, self).dispatch(*args, **kwargs)

class CaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, *args, **kwargs):
        return super(CaseDetail, self).dispatch(*args, **kwargs)

from django.http import JsonResponse

def create_user(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        email = request.GET.get('email')
        password = request.GET.get('password')
        account_number = request.GET.get('account_number')
        
        # 检查必要参数是否已提供
        if not all([username, email, password, account_number]):
            return JsonResponse({'success': False})
        
        # 检查该用户是否已经存在
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False})
        
        # 创建新用户
        user = User.objects.create(username=username, email=email, password=password, account_number=account_number)
        
        # 返回状态和用户名
        return JsonResponse({'success': True, 'username': user.username})
    else:
        return JsonResponse({'success': False})

def login_user(request):
    account = request.GET.get('account_number').strip()
    passw = request.GET.get('password').strip()
    try:
        user = User.objects.get(account_number=account)
        if user.password == passw:
            response = JsonResponse({
            'account_number': user.account_number,
            'username': user.username,
            'logged_in': True
        })
            response.set_cookie('username', user.username, max_age=86400) # 设置一个过期时间，这里设置为1天
            response.set_cookie('account_number', user.account_number, max_age=86400)
            return response
        elif user.password != passw:
            return JsonResponse({'logged_in': False})
    except:
        return JsonResponse({'logged_in': False})

from django.contrib.auth.hashers import make_password

def change_password(request):
    account = request.GET.get('account_number').strip()
    old_password = request.GET.get('old_password').strip()
    new_password = request.GET.get('new_password').strip()

    try:
        user = User.objects.get(account_number=account)

        if user.password != old_password:
            return JsonResponse({'success': False, 'error': 'Incorrect old password.'})

        # 对新密码进行加密
        user.password = make_password(new_password)
        user.save()

        return JsonResponse({'success': True})
    
    except ObjectDoesNotExist:
        return JsonResponse({'success': False, 'error': 'User does not exist.'})

from django.db.models import Q

class ClosestCases_GPA(APIView):
    def get(self, request):
        # 获取查询参数
        gpa = request.GET.get('gpa')

        # 构建查询条件
        cases_higher = Case.objects.filter(gpa__gte=gpa).order_by('gpa')[:25]
        cases_lower = Case.objects.filter(gpa__lte=gpa).order_by('-gpa')[:25]
        cases = list(cases_higher) + list(cases_lower)

        # 序列化并返回案例数据
        serializer = CaseSerializer(cases, many=True)
        
        return Response(serializer.data)
    
class ClosestCases_GRE(APIView):
    def get(self, request):
        # 获取查询参数
        gre_score = request.GET.get('gre_score')

        # 构建查询条件
        cases_higher = Case.objects.filter(gpa__gte=gre_score).order_by('gre_score')[:25]
        cases_lower = Case.objects.filter(gpa__lte=gre_score).order_by('-gre_score')[:25]
        cases = list(cases_higher) + list(cases_lower)

        # 序列化并返回案例数据
        serializer = CaseSerializer(cases, many=True)
        
        return Response(serializer.data)

class ClosestCases_ielts(APIView):
    def get(self, request):
        # 获取查询参数
        ielts_score = request.GET.get('ielts_score')
        print("是代码的问题")
        # 构建查询条件
        cases_higher = Case.objects.filter(gpa__gte=ielts_score).order_by('ielts_score')[:25]
        cases_lower = Case.objects.filter(gpa__lte=ielts_score).order_by('-ielts_score')[:25]
        cases = list(cases_higher) + list(cases_lower)

        # 序列化并返回案例数据
        serializer = CaseSerializer(cases, many=True)
        
        return Response(serializer.data)
    
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from .serializers import ArticleSerializer
from .models import Article

def get_article(request, id):
    article = get_object_or_404(Article, id=id)
    serializer = ArticleSerializer(article)
    return JsonResponse(serializer.data)

from django.http import JsonResponse
from django.db.models import Count
from .models import Article, Like

def article_list(request):
    articles = Article.objects.annotate(like_count=Count('like'))
    data = [
        {
            'id': article.id,
            'title': article.title,
            'author': article.author.username,
            'like_count': article.like_count
        }
        for article in articles
    ]
    return JsonResponse({'data': data})

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from .models import User, Article, Like


def like_article(request, article_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    # Get the authenticated user
    username = request.GET.get('username', '')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=400)

    # Get the article to be liked
    article = get_object_or_404(Article, id=article_id)

    # Check if the user has already liked the article
    if Like.objects.filter(user=user, article=article).exists():
        return JsonResponse({'error': 'User has already liked the article'}, status=400)

    # Create a new like for the article and user
    Like.objects.create(user=user, article=article)

    return JsonResponse({'message': 'Article liked successfully'})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Article, User

@csrf_exempt
def create_article(request):
    if request.method == 'GET':
        author_username = request.GET.get('author_username')
        title = request.GET.get('title')
        content = request.GET.get('content')

        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User does not exist'})

        article = Article(author=author, title=title, content=content)
        article.save()

        return JsonResponse({'success': True, 'message': 'Article created successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Only GET requests are allowed'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Article, Comment

def article_comments(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = Comment.objects.filter(article=article).order_by('-created_at')
    data = [{
        'user': comment.user.username,
        'content': comment.content,
        'created_at': comment.created_at.isoformat()
    } for comment in comments]
    return JsonResponse(data, safe=False)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from .models import Article, Comment, User

@require_http_methods(['GET'])
def create_comment(request, article_id):
    # 获取参数
    username = request.GET.get('username')
    content = request.GET.get('content')
    user = get_object_or_404(User, username=username)
    article = get_object_or_404(Article, id=article_id)

    # 创建评论
    comment = Comment(user=user, article=article, content=content)
    try:
        comment.save()
        return JsonResponse({'status': 'success'})
    except:
        return JsonResponse({'status': 'error'})

from django.shortcuts import render


from django.shortcuts import render

def custom_page_not_found(request, exception=None):
    print("#################################")
    print("#################################")
    print("#################################")
    print("#################################")
    print("#################################")
    print("前端遇到错误，代码成功抛入")
    print("#################################")
    print("#################################")
    print("#################################")
    print("#################################")
    print("#################################")
    return render(request, 'error.html')

def custom_server_error(request, exception=None):
    return render(request, 'error.html')
