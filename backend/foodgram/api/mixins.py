from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class AddingAndDeletingListMixin:
    serializer_class = None
    model_class = None

    def post(self, request, recipe_id):
        user = self.request.user.id
        data = {"user": user, "recipe": recipe_id}
        serializer = self.serializer_class(
            data=data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        user = request.user
        obj = get_object_or_404(
            self.model_class, user=user, recipe__id=recipe_id
        )
        obj.delete()
        model_title = self.model_class._meta.verbose_name.title()
        return Response(
            f"Успешно удалено: {model_title}!", status.HTTP_204_NO_CONTENT
        )
