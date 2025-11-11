from django.db import models
from django.conf import settings

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField()
    creation_date = models.DateTimeField(auto_now_add=True)
    banner = models.ImageField(default='fallback.png', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    def __str__(self):
        return self.title