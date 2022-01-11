from rest_framework import viewsets, generics, permissions
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, UserRegistrationSerializer, FollowSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from recipe.models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter


class CreateProfileView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            profile = get_object_or_404(CustomUser,
                                        username=request.data.get('username'))
            profile.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            profile = get_object_or_404(CustomUser, username=request.user)
            serializer = self.get_serializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class APIFollow(APIView):
    def get(self):
        user = self.request.user
        followers = user.follower.all()
        serializer = FollowSerializer(followers, many=True)
        return Response(serializer.data)