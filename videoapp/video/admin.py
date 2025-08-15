from django.contrib import admin

from .models import Video, VideoFile 

# Register your models here.
admin.site.register(Video)
admin.site.register(VideoFile)