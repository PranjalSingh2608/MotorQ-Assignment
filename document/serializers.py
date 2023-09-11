from rest_framework import serializers
from .models import Document
from django.contrib.auth.models import User

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['unique_id', 'name']

class DocumentCreationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    content = serializers.JSONField()
    shared_with = serializers.ListField(
        child=serializers.CharField(max_length=10)
    )
    def validate_shared_with(self, value):
        users = User.objects.filter(username__in=value)
        if len(users) != len(value):
            invalid_users = set(value) - set(users.values_list('username', flat=True))
            raise serializers.ValidationError(f"Invalid users: {', '.join(invalid_users)}")
        return users
    
class DocumentContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['unique_id', 'name','content']