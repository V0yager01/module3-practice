from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model


User = get_user_model()

QUALITY_CHOICE = {
    "HD": "HD",
    "FHD": "FHD",
    "UHD": "UHD"
}


class Video(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    is_published = models.BooleanField()
    name = models.CharField(max_length=256, blank=False, null=False)
    total_likes = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateField(auto_now_add=True)


class VideoFile(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_files')
    file = models.FileField()
    quality = models.CharField(choices=QUALITY_CHOICE)