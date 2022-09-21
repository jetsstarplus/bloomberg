from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from filesManager.models import Files

class FileManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        field = all