from django.urls import path, include
from rest_framework import routers
from . import views, cron

router = routers.DefaultRouter()
router.register("receipes", views.ReceipesView, basename="receipes")
router.register("gallery", views.GalleryView, basename="gallery")
router.register("why_slowcooker", views.WhySlowcookerView, basename="why_slowcpoker")
router.register("no_idea_receipes", views.NoIdeaReceipesView, basename="no_idea_receipes")

app_name = "api"

urlpatterns = [
    path("", views.home, name="home"),
    path("api/cron/pull-data", cron.cron_pull_data),
    path("v1/", include(router.urls)),
]
