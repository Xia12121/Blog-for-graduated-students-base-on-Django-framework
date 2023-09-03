from django.urls import path
from .views import UserList, CaseList, UserDetail, CaseDetail, login_user, create_user, change_password, ClosestCases_GPA, ClosestCases_GRE, ClosestCases_ielts, get_article,article_list,like_article,create_article,article_comments,login_view,write_blog,blog_list
from . import views
from .views import search,search_articles
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<str:pk>/', UserDetail.as_view(), name='user-detail'),
    #path('cases/', CaseList.as_view(), name='case-list'),
    #path('cases/<str:pk>/', CaseDetail.as_view(), name='case-detail'),
    path('create_user/', create_user, name='create_user'),
    path('login_user/', login_user, name='login_user'),
    path('change_password/', change_password, name='change_password'),
    
    path('closest_cases_GPA/', ClosestCases_GPA.as_view(), name='closest_cases_GPA'),
    path('closest_cases_GRE/', ClosestCases_GRE.as_view(), name='closest_cases_GRE'),
    path('ClosestCases_ielts/', ClosestCases_ielts.as_view(), name='closest_cases_ielts'),
   
    path('articles/<int:id>/', get_article, name='get-article'),
    path('article_list/', article_list, name='article_list'),
    path('article_follow_list/', views.followed_blog_list_follow, name='article_follow_list'),
    #path('articles/<int:article_id>/like', like_article, name='like_article'),
    path('create_article/', create_article, name='create_article'),
    path('articles/<int:article_id>/comments/', article_comments, name='article_comments'),
    path('articles/<int:article_id>/comments/create/', views.create_comment, name='create_comment'),

    
    path('',views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('signup_alumni/', views.signup_alumni, name='signup_alumni'),
    path('write/', views.write_blog, name='write'),
    path('search/', search, name='search'),
    path('blog_list/', views.blog_list, name='blog_list'),
    path('blog/', views.bloger, name='blog'),
    path('login/', views.login_view, name='login'), 
    path('personal_homepage/', views.Personal_homepage, name='homegape'),
    path('write_article/', views.write_article, name='write_article'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path('add_comment/<int:article_id>/', views.write_comment, name='add_comment'),
    path('like/<int:article_id>/', views.like_article_new, name='like_article'),
    path('dislike/<int:article_id>/', views.cancel_like, name='dislike'),
    path('update_personal_statement/', views.update_personal_statement, name='update_personal_statement'),
    path('modify_password_here/', views.modify_password_here, name='modify_password_here'),
    path('homegapg/<str:username>/', views.Personal_homepage_other, name='personal_homepage_other'),
    path('send-message/<str:recipient_username>/', views.send_message, name='send_message'),
    path('feedback/', views.create_feedback, name='create_feedback'),
    path('register/', views.register_view, name='register'),
    path('register_alumni/', views.register_view_alumi, name='register_alumni'),
    path('create_offer/', views.create_offer, name='create_offer'),
    path('offer/<int:pk>/', views.offer_detail, name='offer_detail'),
    path('search_result/', views.search_offers, name='search_result'),
    path('follow/<str:username_idol>/', views.follow, name='follow'),
    path('blog_search/', search_articles, name='search_blog'),
    path('tag_article/<str:tag_name>/', views.tag_articles, name='tag_article'),
    path('management/', views.manage_account, name='management'),
    path('dashboard/', views.dashboard, name='dashboard'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
