from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse
from rest_framework import generics
from .models import Card, Ingredient, Recipe
from .serializers import IngredientSerializer, RecipeSerializer
from .forms import RecipeForm, IngredientFormset


class HomePageView(TemplateView):
    template_name = "zutatenberechner/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cards"] = Card.objects.all()
        return context


class RecipeCreateView(CreateView):
    template_name = "zutatenberechner/create_recipe.html"
    model = Recipe
    form_class = RecipeForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = IngredientFormset()
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = IngredientFormset(self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset)
        )

    def get_success_url(self):
        return reverse("calculator")


class CalculatorView(TemplateView):
    template_name = "zutatenberechner/calculator.html"


class AboutView(TemplateView):
    template_name = "zutatenberechner/about.html"


class ImpressumView(TemplateView):
    template_name = "zutatenberechner/impressum.html"


class GetRecipesAPI(generics.ListAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class GetRecipeAPI(generics.RetrieveAPIView):
    lookup_field = "name"
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class GetIngredientsByRecipeAPI(generics.ListAPIView):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        return Ingredient.objects.filter(recipe=self.kwargs["id"])


class GetCardRecipeAPI(generics.ListAPIView):
    serializer_class = RecipeSerializer

    def get_queryset(self):
        return Card.objects.filter(id=self.kwargs["id"]).first().recipes.all()
