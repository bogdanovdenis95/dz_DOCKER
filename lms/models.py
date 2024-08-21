from django.db import models
from django.conf import settings
from .validators import validate_youtube_url

class Course(models.Model):
    title = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField(validators=[validate_youtube_url])
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'course')
