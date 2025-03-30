from django.db import models

class Crop(models.Model):
    name = models.CharField(max_length=50, unique=True)
    image = models.ImageField(upload_to='crop_images/')
    description = models.TextField()
    crop_type = models.CharField(max_length=100)
    diseases = models.TextField()
    companion = models.TextField(blank=True, null=True)
    pests = models.TextField(blank=True, null=True)
    fertilizer = models.TextField()
    tips = models.TextField(blank=True, null=True)
    spacing = models.TextField(blank=True, null=True)
    watering = models.TextField(blank=True, null=True)
    storage = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

