from rest_framework import viewsets, generics, permissions
from djoser.views import UserViewSet
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer
from recipe.models import Tag, Recipe, Ingredient
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

# class CreateProfileView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     queryset = User.objects.all()
#     # permission_classes = (permissions.AllowAny,)
#
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             profile = get_object_or_404(User,
#                                         username=request.data.get('username'))
#             # profile.confirmation_code = mail(profile)
#             profile.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class CreateProfileView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer
#     queryset = User.objects.all()
#     permission_classes = (permissions.AllowAny,)
#
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             profile = get_object_or_404(User,
#                                         username=request.data.get('username'))
#             profile.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class Login(generics.CreateAPIView):
#     def post(self, request):
#         serializer = TokenSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors,
#                             status=status.HTTP_400_BAD_REQUEST)
#         profile = get_object_or_404(Profile,
#                                     username=request.data.get('username'))
#         confirmation_code = request.data.get('confirmation_code')
#         if profile.confirmation_code != confirmation_code:
#             return Response('Неверный код подтверждения',
#                             status=status.HTTP_400_BAD_REQUEST)
#         refresh = RefreshToken.for_user(profile)
#         token = str(refresh.access_token)
#         return Response({'token': token}, status=status.HTTP_201_CREATED)


# class Logout(APIView):
#     def get(self, request, format=None):
#         # simply delete the token to force a login
#         request.user.auth_token.delete()
#         return Response(status=status.HTTP_200_OK)




class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
