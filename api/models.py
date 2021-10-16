from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify


class Receipe(models.Model):
    receipe_id = models.IntegerField(unique=True)
    url = models.CharField(max_length=255)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    serving_size = models.CharField(max_length=10)
    preparing_time = models.CharField(max_length=25)
    time_on_high = models.CharField(max_length=25)
    time_on_low = models.CharField(max_length=25)
    receipe_ingredients = models.TextField()
    receipe_how_to = models.TextField()
    views = models.IntegerField(default=1)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return " ".join([str(self.receipe_id), self.name])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ["receipe_id", "slug"]


class ReceipeImage(models.Model):
    receipe = models.ForeignKey(
        Receipe, on_delete=models.CASCADE, related_name="images"
    )
    image = models.CharField(max_length=255)

    def __str__(self):
        return f"{settings.SITE_URL}{settings.MEDIA_URL}img/{self.image}"


class WhySlowcooker(models.Model):
    heading = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=255)
    icon = models.CharField(max_length=100)

    def __str__(self):
        return self.heading
