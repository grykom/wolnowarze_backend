from django.contrib import admin
from .models import recipe, recipeImage, WhySlowcooker


admin.site.register(recipe)
admin.site.register(recipeImage)
admin.site.register(WhySlowcooker)