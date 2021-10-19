from django.urls import path
from . import views, cron
app_name = "api"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/cron/pull-data", cron.cron_pull_data),

    path("v1/no_idea_receipes", views.NoIdeaReceipesView.as_view({'get': 'list'}), name="no_idea_receipes"),
    path("v1/why_slowcooker", views.WhySlowcookerView.as_view({'get': 'list'}), name="why_slowcooker"),
    path("v1/gallery", views.GalleryView.as_view({'get': 'list'}), name="gallery"),

    path("v1/receipes", views.ReceipesView.as_view({'get': 'list'}), name="receipes_list"),
    path("v1/receipes/<int:receipe_id>", views.ReceipesView.as_view({'get': 'retrieve'}), name="receipe"),
    path("v1/receipes/<int:receipe_id>/likes_<str:up_down>", views.ReceipesView.as_view({'post': 'likes'}), name="receipe_likes"),
]
