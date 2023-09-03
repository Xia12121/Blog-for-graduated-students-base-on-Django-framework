from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
import os
from django.utils.html import format_html, mark_safe
from django.conf import settings

class User(models.Model):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    account_number = models.CharField(primary_key=True, max_length=50)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    personal_statement = models.CharField(max_length=255, default='This person is lazy and has not written anything.')
    fans = models.ManyToManyField("self", symmetrical=False, related_name="idols")

    def __str__(self):
        return self.username

class Case(models.Model):
    case_number = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    graduate_to = models.CharField(max_length=50)
    employed = models.BooleanField(default=False)
    ielts_score = models.DecimalField(max_digits=4, decimal_places=2)
    gre_score = models.IntegerField()
    notes = models.TextField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.case_number:
            # Get the highest case number and add 1
            max_case_number = Case.objects.aggregate(models.Max('case_number'))['case_number__max'] or 0
            self.case_number = str(int(max_case_number) + 1).zfill(4)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_articles')
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    likes = models.ManyToManyField(User, through='Like', related_name='liked_articles')
    is_alumni = models.BooleanField(default=False)  # 添加是否是校友所写字段
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')  # 添加标签字段

    class Meta:
        ordering = ['id']

    def get_liked_user(self):
        likes_user = self.likes.all()
        return likes_user
    
    @property
    def comments(self):
        return Comment.objects.filter(article=self)

    def save(self, *args, **kwargs):
        if not self.id:
            # Get the highest ID value and add 1
            max_id = Article.objects.aggregate(models.Max('id'))['id__max'] or 0
            self.id = max_id + 1
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}: {self.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f'{self.user.username} liked {self.article.title}'

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.username} commented on {self.article.title}"

    
class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.sender.username} sent a message to {self.recipient.username}"
    
class Feedback(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_feedbacks')
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender.username} sent feedback on {self.sent_at}"

class TeamIntroduction(models.Model):
    description = models.TextField()

    def save(self, *args, **kwargs):
        if not self.pk and TeamIntroduction.objects.exists():
            raise ValidationError('There can be only one TeamIntroduction instance')
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Team Introduction"
    
class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='avatars/',default='avatars/default.png')
    area_of_responsibility = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class worker(User):
    task_statement = models.CharField(max_length=255, default='')
    real_name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.username
    
class FeaturedArticle(Article):
    admin_comment = models.CharField(max_length=255, null=True, blank=True)
    cover_url = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "精选文章"
        verbose_name_plural = "精选文章"

    def __str__(self):
        return f"{self.id}: {self.title} (精选文章)"
    
class Alumni(User):
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    graduation_destination = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.username} (Alumni)"
    

def get_upload_to(instance, filename):
    return os.path.join('app_name/static/offers', str(instance.offer_id), filename)


class Offer(models.Model):
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    ielts_score = models.DecimalField(max_digits=4, decimal_places=2)
    institution = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=False)
    offer_image = models.ImageField(upload_to='offers/', default='offers/default.png')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applied_offers')
    received_at = models.DateTimeField(auto_now_add=True)
    offer_id = models.AutoField(primary_key=True)

    class Meta:
        ordering = ['offer_id']

    def save(self, *args, **kwargs):
        if not self.offer_id:
            # Get the highest ID value and add 1
            max_id = Offer.objects.aggregate(models.Max('offer_id'))['offer_id__max'] or 0
            self.offer_id = max_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.offer_id}: {self.major} at {self.institution}"
    


'''    def offer_image_tag(self):
        return mark_safe('<img src="%s" style="max-width: 150px; max-height: 150px" />' % self.offer_image_url())

    offer_image_tag.short_description = 'Offer Image'''
    
class UserLoginRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    login_ip = models.CharField(max_length=45)

    class Meta:
        ordering = ['-login_time']

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time} from {self.login_ip}"
    
class Major(models.Model):
    name = models.CharField(max_length=100)

class School(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    majors = models.ManyToManyField(Major)