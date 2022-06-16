from django.contrib import admin
from .models import Recipe, Ingredient, Card


class IngredientsInline(admin.TabularInline):
    model = Ingredient


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientsInline]


admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Card)
