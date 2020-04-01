from django.db import models
from datetime import datetime
from ckeditor.fields import RichTextField

# Create your models here.
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to='blog/images/')
    caption = models.TextField()
    content = RichTextField()
    date_time = models.DateTimeField(default=datetime.now)


    def __str__(self):
        return f"{self.title}"
