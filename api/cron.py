from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseBadRequest, HttpResponse
from django.conf import settings

from .utils import CrockPotRecipe, get_last_crockpot_receipe_id
from .models import Receipe, ReceipeImage


def cron_pull_data(request):
    try:
        range_start = Receipe.objects.latest("receipe_id").receipe_id + 1
    except ObjectDoesNotExist:
        range_start = 1

    range_crockpot_limit = get_last_crockpot_receipe_id()
    if not range_crockpot_limit:
        return HttpResponseBadRequest("Crockpot down?")

    cron_fetch_limit = (
        settings.CRON_FETCH_LIMIT
        if not request.GET.get("nolimit")
        else range_crockpot_limit
    )

    receipe_creted = []
    for i in range(range_start, range_crockpot_limit):
        receipe = CrockPotRecipe(i)
        receipe_data = receipe.get_receipe_data()

        if receipe_data:
            new_receipe = Receipe.objects.create(**receipe_data)
            receipe_creted.append(new_receipe)

            receipe_image = receipe.get_receipe_images()
            for image in receipe_image["images"]:
                ReceipeImage.objects.create(receipe=new_receipe, image=image)

            cron_fetch_limit -= 1
            if not cron_fetch_limit:
                break

    return HttpResponse([f"{r} created!<br/>" for r in receipe_creted])
