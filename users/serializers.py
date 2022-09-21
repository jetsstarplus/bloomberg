from importlib.metadata import files
from django.contrib.auth.models import User

from rest_framework import serializers

from filesManager.models import Files

class UserSerializer(serializers.ModelSerializer):
    files = serializers.PrimaryKeyRelatedField(many=True, queryset=Files.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'files', 'email']