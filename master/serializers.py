from .models import *
from rest_framework import serializers

class RatingGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

class RecipeSerializer(serializers.ModelSerializer):
    ratings = RatingGetSerializer(many=True)
    class Meta:
        model = Recipe
        fields = "__all__"

class AddUpdateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        exclude = ['seller']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        exclude = ['customer']

