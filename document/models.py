from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.JSONField()
    unique_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.name
