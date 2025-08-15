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
    """ Модель для видео """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    is_published = models.BooleanField()
    name = models.CharField(max_length=256, blank=False, null=False)
    total_likes = models.IntegerField(validators=[MinValueValidator(0)])
    created_at = models.DateField(auto_now_add=True)


class VideoFile(models.Model):
    """ Модель для файлов """
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='video_files')
    file = models.FileField()
    quality = models.CharField(choices=QUALITY_CHOICE)


class Like(models.Model):
    """ Модель реакций """
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                'video',
                'user'
            ], name='unique_video_user_pair_contraint')
        ]