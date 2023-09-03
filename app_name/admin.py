from django.contrib import admin
from django import forms
from django.db.models import Count
from app_name.models import User, Case, Article, Like, Comment, PrivateMessage, Feedback, TeamIntroduction, TeamMember, worker, FeaturedArticle,Alumni,Offer,Tag,UserLoginRecord,Major, School
from django.utils.html import format_html, mark_safe
from django.utils.text import format_lazy
from django.urls import path
from django.templatetags.static import static
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
admin.site.site_header = 'GPS services admin'  # 设置header
admin.site.site_title = 'GPS services admin'   # 设置title
admin.site.index_title = 'GPS services admin'

class MyAdminSite(admin.AdminSite):
    site_header = 'My Admin Site'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('dashboard/', self.admin_view(self.views.dashboard), name='dashboard'),
        ]
        return my_urls + urls

    def my_custom_page(self, request):
        # Your custom view logic goes here.
        context = dict(
            self.each_context(request),
            # Add extra context variables here.
        )
        return self.render_template('src/dashboard.html', context)


def show_dashboard(modeladmin, request, queryset):
    return HttpResponseRedirect(reverse('dashboard'))
show_dashboard.short_description = "显示控制面板"

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'email', 'account_number', 'avatar_tag')
    readonly_fields = ('avatar_tag',)
    filter_vertical = ('fans',)

    def avatar_tag(self, obj):
        if obj.avatar:
            avatar_url = format_lazy('{}{}', static(''), obj.avatar.name)
            return format_html('<img src="{}" width="100" height="100" />', avatar_url)
        else:
            return 'No Avatar'
    avatar_tag.short_description = 'Avatar'
    actions = [show_dashboard]

admin.site.register(User, UserAdmin)
admin.site.register(Case)
admin.site.register(Like)



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'like_count', 'created_at', 'is_alumni')
    list_display_links = ('id', 'title')
    list_filter = ('author', 'created_at', 'is_alumni')  # 添加 is_alumni 到筛选条件
    search_fields = ('id', 'title', 'content')
    ordering = ('id',)

    def like_count(self, obj):
        return obj.likes.count()  # 将 obj.like_set 改为 obj.likes
    like_count.short_description = '点赞数'

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(num_likes=Count('likes'))
        return queryset

    def is_alumni(self, obj):
        return obj.is_alumni  # 添加 is_alumni 字段的显示
    is_alumni.boolean = True
    is_alumni.short_description = '是否是校友'
    actions = [show_dashboard]
    


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'article', 'created_at')
    list_display_links = ('id',)
    list_filter = ('user', 'article', 'created_at')
    search_fields = ('id', 'user__username', 'article__title', 'content')
    ordering = ('id',)
    actions = [show_dashboard]

@admin.register(PrivateMessage)
class PrivateMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'sent_at')
    actions = [show_dashboard]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'content', 'sent_at')
    list_filter = ('sent_at', 'sender__username')
    search_fields = ('content', 'sender__username')
    actions = [show_dashboard]

admin.site.register(Feedback, FeedbackAdmin)

class TeamIntroductionAdmin(admin.ModelAdmin):
    list_display = ('description',)
    actions = [show_dashboard]

class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'area_of_responsibility')
    actions = [show_dashboard]

admin.site.register(TeamIntroduction, TeamIntroductionAdmin)
admin.site.register(TeamMember, TeamMemberAdmin)

@admin.register(worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ('username', 'real_name', 'email', 'task_statement')
    search_fields = ('username', 'real_name', 'email', 'task_statement')
    list_filter = ('username', 'real_name', 'email')
    actions = [show_dashboard]

@admin.register(FeaturedArticle)
class FeaturedArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'admin_comment', 'cover_url')
    list_filter = ('author',)
    search_fields = ('title', 'content')
    actions = [show_dashboard]

@admin.register(Alumni)
class AlumniAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'account_number', 'avatar', 'personal_statement', 'gpa', 'graduation_destination')
    search_fields = ('username', 'email', 'account_number')
    actions = [show_dashboard]

class OfferAdmin(admin.ModelAdmin):
    list_display = ('offer_id', 'applicant', 'institution', 'major', 'received_at', 'is_valid','offer_image_tag')
    list_filter = ('is_valid',)
    search_fields = ('applicant__username', 'institution', 'major')
    actions = ['make_valid', 'make_invalid']

    def make_valid(self, request, queryset):
        queryset.update(is_valid=True)
    make_valid.short_description = "Mark selected offers as valid"

    def make_invalid(self, request, queryset):
        queryset.update(is_valid=False)
    make_invalid.short_description = "Mark selected offers as invalid"

    def offer_image_tag(self, obj):
        if obj.offer_image:
            avatar_url = format_lazy('{}{}', static(''), obj.offer_image.name)
            return format_html('<img src="{}" width="100" height="100" />', avatar_url)
        else:
            return 'No Avatar'
    offer_image_tag.short_description = 'offer_image_tag'
    

    

    

admin.site.register(Offer, OfferAdmin)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # 在列表中显示id和名称字段
    search_fields = ('name',)  # 添加搜索栏，可以根据名称搜索标签

@admin.register(UserLoginRecord)
class UserLoginRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'login_ip')
    list_filter = ('user', 'login_time')
    search_fields = ('user__username', 'login_ip')
    readonly_fields = ('user', 'login_time', 'login_ip')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    
class MajorInline(admin.TabularInline):
    model = School.majors.through
    verbose_name = 'Major'
    verbose_name_plural = 'Majors'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'major':
            kwargs['queryset'] = Major.objects.all().order_by('id')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    search_fields = ('name', 'country')
    inlines = [MajorInline]

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.form.base_fields['major'].label = 'Name'
        return formset

    class Meta:
        ordering = ['name']

class SchoolInline(admin.TabularInline):
    model = School.majors.through

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'school_count')

    search_fields = ('name',)
    inlines = [SchoolInline]

    def school_count(self, obj):
        return obj.school_set.count()

    school_count.short_description = 'Number of Schools'
