from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['unique_id', 'name']

class DocumentCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    content = serializers.JSONField()