from django.urls import path
from . import views, cron

app_name = "api"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/cron/pull-data", cron.cron_pull_data),
    path(
        "v1/no_idea_recipes",
        views.NoIdearecipesView.as_view({"get": "list"}),
        name="no_idea_recipes",
    ),
    path(
        "v1/why_slowcooker",
        views.WhySlowcookerView.as_view({"get": "list"}),
        name="why_slowcooker",
    ),
    path("v1/gallery", views.GalleryView.as_view({"get": "list"}), name="gallery"),
    path(
        "v1/recipes", views.recipesView.as_view({"get": "list"}), name="recipes_list"
    ),
    path(
        "v1/recipes/<int:recipe_id>/",
        views.recipesView.as_view({"get": "retrieve"}),
        name="recipe",
    ),
    path(
        "v1/recipes/<int:recipe_id>/likes_<str:up_down>",
        views.recipesView.as_view({"post": "likes"}),
        name="recipe_likes",
    ),
]
