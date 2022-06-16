from django.db import models


class Recipe(models.Model):
    name = models.CharField("Rezeptname", max_length=100, unique=True)
    description = models.TextField("Beschreibung", max_length=1000)

    def __str__(self):
        return f"{self.name}"


class Ingredient(models.Model):
    UNITS = (
        ("l", "Liter"),
        ("ml", "Milliliter"),
        ("g", "Gramm"),
        ("kg", "Kilogramm"),
        ("stk", "Stück"),
    )
    name = models.CharField(max_length=30)
    unit = models.CharField(max_length=10, choices=UNITS)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    recipe = models.ForeignKey(
        Recipe, related_name="ingredients", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} ({self.quantity} {self.unit})"


class Card(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    picture = models.ImageField(upload_to="zutatenberechner/images/cards/")
    recipes = models.ManyToManyField(Recipe)

    def __str__(self):
        return f"{self.title}"
