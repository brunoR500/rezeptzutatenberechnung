from django import forms
from django.forms.models import inlineformset_factory
from .models import Recipe, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = "__all__"


IngredientFormset = inlineformset_factory(Recipe, Ingredient, fields="__all__", extra=1)