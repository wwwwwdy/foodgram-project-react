from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import CustomUser, Follow
from .serializers import (CustomUserSerializer, UserRegistrationSerializer,
                          UserSerializer)


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

    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.filter(id=request.user.id)
        serializer = UserSerializer(queryset, many=True)
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
