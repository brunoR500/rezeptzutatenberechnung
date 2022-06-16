from django.urls import path
from . import views


urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    path("berechner/", views.CalculatorView.as_view(), name="calculator"),
    path("rezeptersteller/", views.RecipeCreateView.as_view(), name="create_recipe"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("impressum/", views.ImpressumView.as_view(), name="impressum"),
    path("api/recipes/", views.GetRecipesAPI.as_view()),
    path("api/recipe/<str:name>", views.GetRecipeAPI.as_view()),
    path("api/ingredients/<int:id>", views.GetIngredientsByRecipeAPI.as_view()),
    path("api/card/<int:id>", views.GetCardRecipeAPI.as_view()),
]
