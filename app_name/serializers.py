from rest_framework import serializers
from .models import User, Case,Article

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['account_number', 'username', 'email', 'password']

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = ['case_number', 'name', 'gpa', 'graduate_to', 'employed', 'ielts_score', 'gre_score', 'notes']

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'