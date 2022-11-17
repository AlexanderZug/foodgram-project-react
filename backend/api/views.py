import io
from datetime import datetime

from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from recipes.models import (
    Favourite,
    Ingredient,
    IngredientInRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeShortSerializer,
    RecipeWriteSerializer,
    TagSerializer,
)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_to(Favourite, request.user, pk)
        return self.delete_from(Favourite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_to(ShoppingCart, request.user, pk)
        return self.delete_from(ShoppingCart, request.user, pk)

    def add_to(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response(
                {'errors': 'Рецепт добавлен'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShortSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_from(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт удален'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=HTTP_400_BAD_REQUEST)

        ingredients = (
            IngredientInRecipe.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .values('ingredient__name', 'ingredient__measurement_unit', 'recipe__image')
            .annotate(amount=Sum('amount'))
        )

        today = datetime.today()
        shopping_list = (
            f'Список покупок: {user.get_full_name()}\n'
            f'Дата: {today:%Y-%m-%d}\n'
        )
        shopping_list += '\n'.join(
            [
                f'-- {ingredient["ingredient__name"]} '
                f'-- ({ingredient["ingredient__measurement_unit"]}) '
                f'-- {ingredient["amount"]} '.title()
                for ingredient in ingredients
            ]
        )
        filename = f'{user.username}_shopping_list.pdf'

        buffer = io.BytesIO()
        pdf_to_user = canvas.Canvas(buffer, pagesize=A4)
        pdfmetrics.registerFont(TTFont('TimesNewRoman', 'Times New Roman.ttf'))
        pdf_to_user.setFont('TimesNewRoman', 14)
        for k, v in enumerate(shopping_list.split('\n')):
            pdf_to_user.drawString(45, 800 - int(str(k) + str(10)), v)
        image = ImageReader('media/' + ingredients[0].get('recipe__image'))
        pdf_to_user.drawImage(image, 450, 50, 100, 100)
        pdf_to_user.showPage()
        pdf_to_user.save()

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=filename)
