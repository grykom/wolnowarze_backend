from django.contrib import admin
from .models import Recipe, RecipeImage, WhySlowcooker


admin.site.register(Recipe)
admin.site.register(RecipeImage)
admin.site.register(WhySlowcooker)