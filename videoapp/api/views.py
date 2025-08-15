from django.db import transaction
from django.db.models import Q, F, OuterRef, Sum, Subquery
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .permissions import IsAuthor
from .serializers import VideoSerializer, VideoIdsSerializer, VideoStatisticsSerializer
from video.models import Video, User
from like.models import Like


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return Video.objects.all()

        elif self.request.user.is_authenticated:
            return Video.objects.filter(
                Q(is_published=True) | Q(owner=self.request.user)
            )

        return Video.objects.filter(is_published=True)

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'ids':
            return VideoIdsSerializer
        elif self.action in ['statistics_subquery', 'statistics_group_by']  :
            return VideoStatisticsSerializer
        return VideoSerializer

    @action(detail=True, methods=['POST', 'DELETE'], permission_classes=[IsAuthenticated])
    def likes(self, request, pk):
        video = self.get_object()
        if request.method == 'POST':
            with transaction.atomic():
                try:
                    like = Like.objects.create(user=request.user, video=video)
                    video.total_likes = F('total_likes') + 1
                    video.save()
                except IntegrityError:
                    return Response({"detail": "Лайк уже существует"},
                                    status=status.HTTP_400_BAD_REQUEST)


        elif request.method == 'DELETE':
            with transaction.atomic():
                like = get_object_or_404(Like, video=video)
                like.delete()
                video.total_likes = F('total_likes') - 1
                video.save() 
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAdminUser])
    def ids(self, request):
        serializer = self.get_serializer_class()
        video = serializer(self.get_queryset(), many=True)
        return Response(video.data)


    @action(methods=['GET'], detail=False, permission_classes=[IsAdminUser])
    def statistics_subquery(self, request):

        like_sum = (
            Video.objects
            .filter(owner=OuterRef("id"),
                    is_published=True)
            .values("owner")
            .annotate(like_sum=Sum("total_likes"))
            .values("like_sum")
        )
        users = User.objects.values("username").annotate(like_sum=like_sum).order_by("-like_sum")
        serializer = self.get_serializer_class()
        statistic = serializer(users, many=True)
        return Response(statistic.data)
    

    @action(["GET"], detail=False, permission_classes=[IsAdminUser])
    def statistics_group_by(self, request, *args, **kwargs):
        videos = Video.objects.filter(is_published=True).values(username=F('owner__username')).annotate(like_sum=Sum('total_likes')).values('username','like_sum').order_by('-like_sum')
        serializer = self.get_serializer(videos, many=True)
        return Response(serializer.data)