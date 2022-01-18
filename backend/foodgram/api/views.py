from rest_framework import viewsets
from .serializers import (TagSerializer, RecipeSerializer, IngredientSerializer, RecipeListSerializer,
                          FavoriteSerializer)
from recipe.models import Tag, Recipe, Ingredient, Favorite
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
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

class CreateDestroyListViewSet(CreateModelMixin,
                               DestroyModelMixin,
                               ListModelMixin,
                               viewsets.GenericViewSet):
    pass


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
    serializer_class = RecipeListSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return RecipeSerializer
        return RecipeListSerializer

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


# class APIFavorite(CreateDestroyListViewSet):
#     queryset = Recipe.objects.all()
#     serializer_class = RecipeListSerializer
#     permission_classes = (IsAuthenticated,)
#     pagination_class = PageNumberPagination
#     filter_backends = ()
    # def post(self, request, serializer, pk):
    #     user = self.request.user
    #     recipe = get_object_or_404(Recipe, id=pk)
    #     serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer(user=user, recipe=recipe)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    #
    # def destroy(self, Des):
    #     recipe = get_object_or_404(Recipe, id=self.kwargs.get('recipe_id'))
    #     self.perform_destroy(recipe)
# class AddingAndDeletingListMixin:
#     serializer_class = None
#     model_class = None
#
#     def post(self, request, recipe_id):
#         user = request.user.id
#         data = {"user": user, "recipe": recipe_id}
#         serializer = self.serializer_class(
#             data=data,
#             context={"request": request},
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status.HTTP_201_CREATED)
#
#     def delete(self, request, recipe_id):
#         user = request.user
#         obj = get_object_or_404(
#             self.model_class, user=user, recipe__id=recipe_id
#         )
#         obj.delete()
#         model_title = self.model_class._meta.verbose_name.title()
#         return Response(
#             f"Успешно удалено: {model_title}!", status.HTTP_204_NO_CONTENT
#         )
#
#
# class FavoriteViewSet(AddingAndDeletingListMixin, APIView):
#     serializer_class = FavoriteRecipeSerizlizer
#     model_class = Favorite

#
# class PurchaseListView(AddingAndDeletingListMixin, APIView):
#     serializer_class = PurchaseListSerializer
#     model_class = PurchaseList

class FavoriteViewSet(APIView):
    def post(self, request, recipe_id):
        user = request.user.id
        print(request)
        print(recipe_id)
        data = {"user": user, "recipe": recipe_id}
        print(data)
        serializer = FavoriteSerializer(
            data=data,
            context={"request": request},
        )
        # print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        favorite_recipe = get_object_or_404(
            Favorite, user=user, recipe__id=recipe_id
        )
        favorite_recipe.delete()
        return Response(
            "Рецепт удален из избранного", status.HTTP_204_NO_CONTENT
        )
