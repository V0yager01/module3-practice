from rest_framework import serializers

from video.models import Video, User, VideoFile


class VideoFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoFile
        fields = ('file',
                  'quality')


class VideoSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='owner.username', read_only=True)
    video_files = VideoFileSerializer(many=True)
    class Meta:
        model = Video
        fields = (
            'owner',
            'video_files',
            'name',
            'total_likes',
            'created_at'
        )


class VideoIdsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = ['id']


class VideoStatisticsSerializer(serializers.Serializer):
    username = serializers.CharField()
    like_sum = serializers.IntegerField()    

    class Meta:
        fields = ['username',
                  'like_sum']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)