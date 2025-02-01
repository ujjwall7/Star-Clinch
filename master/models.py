from django.contrib.auth.models import AbstractUser
from django.db import models

from django.dispatch import receiver
from django.db.models.signals import post_save
from .task import resize_and_convert_to_webp

def webpConverter(instance, filename):
    if filename.find('.') >= 0:
        dot_index = (len(filename) - filename.rfind('.', 1)) * (-1)
        filename = filename[0:dot_index]
    filename = '{}.{}'.format(filename, 'webp')
    return filename


class User(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

# Recipe Model
class Recipe(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Recipe)
def convert_image(sender, instance, **kwargs):
    print("🚀 Signal Triggered!")  # Debugging ke liye
    print(f"{instance.image.path = }")  
    resize_and_convert_to_webp.delay(instance.image.path, instance.id)

# Rating Model
class Rating(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.customer.username} - {self.recipe.name}: {self.rating}"