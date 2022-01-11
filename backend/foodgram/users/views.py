from rest_framework import viewsets, generics, permissions
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, UserRegistrationSerializer, FollowSerializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from users.models import CustomUser, Follow
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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


class FollowViewSet(viewsets.ViewSet):
    serializer_class = FollowSerializers

    def get_queryset(self):
        """Filter queryset by following user."""
        followers = self.request.user.follower.all()
#         followers = self.request.user.follower.all()
        return followers

    def perform_create(self, serializer):
        user = self.request.user
        following = get_object_or_404(CustomUser, pk=serializer.initial_data.get('id'))
        serializer.save(user=user, author=following)
#     @action(detail=True, methods=['post'])
#     def add_followers(self, request, user_id, following_id):

#     def post(self, request, pk=None):
#         user = self.request.user
#         author = get_object_or_404(CustomUser, id=self.kwargs['pk'])
#         serializer = FollowSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user, author=author)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FollowViewSet(APIView):
#     def post(self, request, pk=None):
#         user = self.request.user
#         author = get_object_or_404(CustomUser, id=self.kwargs['pk'])
#         serializer = FollowSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=user, author=author)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class FollowViewSet(viewsets.ModelViewSet):
#     serializer_class = FollowSerializer
#     # filter_backends = (SearchFilter,)
#     # search_fields = ('following__username',)
#
#     def get_queryset(self):
#         return self.request.user.follower.all()
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class UserFollowingViewSet(viewsets.ModelViewSet):
#
#     permission_classes = (IsAuthenticatedOrReadOnly,)
# #     serializer_class = UserFollowingSerializer
#     queryset = Follow.objects.all()