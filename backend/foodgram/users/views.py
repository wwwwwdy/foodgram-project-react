from tkinter.messagebox import NO
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from html5lib import serialize
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser, Follow
from .serializers import (CustomUserSerializer, UserRegistrationSerializer, FollowUserSerializer,
                          FollowUserCreateSerializer)
from api.pagination import CustomPageNumberPagination

class CreateProfileView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer


class ProfileUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'

    @action(detail=False,
            methods=['get', 'patch'],
            permission_classes=(permissions.IsAuthenticated,))
    def me(self, request):
        if request.method == 'GET':
            profile = get_object_or_404(CustomUser,
                                        username=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(request.user,
                                          data=request.data,
                                          partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class UserFollowingViewSet(viewsets.ModelViewSet):

    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowUserSerializer

    # def get_serializer_class(self):
    #     if self.action in ('list', 'retrieve'):
    #         return FollowUserSerializer
    #     return FollowUserCreateSerializer

    def get_queryset(self, *args, **kwargs):
        # user_id = self.request.user.id
        return CustomUser.objects.filter(following__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.filter(following__user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowUserSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = FollowUserSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, id, *args, **kwargs):
        user = CustomUser.objects.get(id=request.user.id)
        follower = CustomUser.objects.get(id=id)
        obj, _ = Follow.objects.update_or_create(
            user=user,
            following=follower)
        return Response(status=201)

    @action(methods=['delete'], detail=False)
    def delete(self, request, id):
        Follow.objects.filter(
            user=request.user.id,
            following=id).delete()
        return Response(status=201)

class SubscriptionsView(generics.ListAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowUserSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        return Follow.objects.filter(user=user_id)
    
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     paginator = CustomPageNumberPagination
    #     print(request)
    #     page = paginator.paginate_queryset(queryset, request)
    #     if page is not None:
    #         serializer = FollowUserSerializer(page, many=True, context={'request': request})
    #         return paginator.get_paginated_response(serializer.data)
    #     else:
    #         serializer = FollowUserSerializer(queryset, many=True, context={'request': request})
    #     return Response(serializer.data, status=status.HTTP_200_OK)
