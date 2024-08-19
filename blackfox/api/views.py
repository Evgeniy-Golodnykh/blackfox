from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.permissions import IsAdmin, IsCoach
from api.serializers import (
    BodyStatsDiarySerializer, CreateUpdateBodyStatsDiarySerializer,
    CreateUpdateProjectSerializer, FoodDiarySerializer, ProjectSerializer,
)
from fatsecret.tools import get_fooddiary_objects
from training.models import BodyStatsDiary, FoodDiary, Project

User = get_user_model()
fatsecret_account_not_exists_message = 'Please link your Fatsecret account'
fatsecret_error_message = 'Fatsecret error: {error}'
project_not_exists_message = 'Please create a project for current user'


class BodyStatsDiaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user', 'date']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateBodyStatsDiarySerializer
        return BodyStatsDiarySerializer

    def get_queryset(self):
        if self.request.user.role == 'user':
            return BodyStatsDiary.objects.filter(user=self.request.user)
        return BodyStatsDiary.objects.all()


class FoodDiaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = FoodDiarySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user', 'date']

    def get_queryset(self):
        if self.request.user.role == 'user':
            return FoodDiary.objects.filter(user=self.request.user)
        return FoodDiary.objects.all()

    def create(self, request):
        username = request.query_params.get('user')
        if username:
            user = get_object_or_404(User, username=username)
        else:
            user = request.user
        if not user.fatsecret_token or not user.fatsecret_secret:
            return Response(
                {'message': fatsecret_account_not_exists_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not Project.objects.filter(user=user).exists():
            return Response(
                {'message': project_not_exists_message},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            objs = get_fooddiary_objects(user)
        except KeyError as error:
            return Response(
                {'message': fatsecret_error_message.format(error=error)},
                status=status.HTTP_400_BAD_REQUEST
            )
        FoodDiary.objects.bulk_create(objs=objs)
        return Response(FoodDiarySerializer(objs, many=True).data)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdmin | IsCoach]
    queryset = Project.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['user', 'coach', 'start_date']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return CreateUpdateProjectSerializer
        return ProjectSerializer
