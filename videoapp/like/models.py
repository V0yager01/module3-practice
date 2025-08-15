from django.db import models

from video.models import Video, User

class Like(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=[
                'video',
                'user'
            ], name='unique_video_user_pair_contraint')
        ]
    
       