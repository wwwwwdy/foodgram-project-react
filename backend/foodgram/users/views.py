from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPageNumberPagination
from users.models import CustomUser, Follow
from .serializers import (CustomUserSerializer, FollowUserCreateSerializer,
                          FollowUserSerializer, UserRegistrationSerializer)


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

    def get_queryset(self, *args, **kwargs):
        # user_id = self.request.user.id
        return CustomUser.objects.filter(following__user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.filter(following__user=self.request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = FollowUserSerializer(
                page, many=True, context={'request': request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = FollowUserSerializer(
            queryset, many=True, context={'request': request}
        )
        return Response(serializer.data)


class CreateFollow(APIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsAuthenticated,)
    serializer_class = FollowUserCreateSerializer

    def post(self, request, id):
        user = self.request.user
        following = get_object_or_404(CustomUser, id=id)
        data = {'user': user.id, 'following': following.id}
        serializer = FollowUserCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, following=following)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        Follow.objects.filter(
            user=request.user.id,
            following=id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
