from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings

from .utils import CrockPotRecipe, get_last_crockpot_recipe_id
from .models import recipe, recipeImage


def cron_pull_data(request):
    try:
        range_start = recipe.objects.latest("recipe_id").recipe_id + 1
    except ObjectDoesNotExist:
        range_start = 1

    range_crockpot_limit = get_last_crockpot_recipe_id()
    if not range_crockpot_limit:
        return HttpResponseBadRequest("Crockpot down?")

    cron_fetch_limit = (
        settings.CRON_FETCH_LIMIT
        if not request.GET.get("nolimit")
        else range_crockpot_limit
    )

    recipe_creted = []
    for i in range(range_start, range_crockpot_limit):
        recipe = CrockPotRecipe(i)
        recipe_data = recipe.get_recipe_data()

        if recipe_data:
            new_recipe = recipe.objects.create(**recipe_data)
            recipe_creted.append(new_recipe)

            recipe_image = recipe.get_recipe_images()
            for image in recipe_image["images"]:
                recipeImage.objects.create(recipe=new_recipe, image=image)

            cron_fetch_limit -= 1
            if not cron_fetch_limit:
                break

    return HttpResponse([f"{r} created!<br/>" for r in recipe_creted])
